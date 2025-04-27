import os
import re
import io
from datetime import datetime
import tempfile
import requests
from google import genai
from pydub import AudioSegment       # pip install pydub
import simpleaudio as sa             # pip install simpleaudio

# === 1. Gemini 設定（不動） ===
API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyBm5DB9zryMyQyqFJc5icl3u9uKAxDBHQM")
genai_client = genai.Client(api_key=API_KEY)

SYSTEM_PROMPT = """
你是 FEniX 的主唱與團長「徐彭臒（MAX）」，1999年出生的台灣男偶像。
請用 MAX 的風格回答粉絲問題，要自然、口語化、充滿溫度，偶爾可以講幹話或打趣。
不要有任何表情符號。
如果接收到的文字是日文，回覆請用日文
"""

def chat_and_stream(user_text: str) -> str:
    chat = genai_client.chats.create(model="gemini-2.0-flash")
    prompt = SYSTEM_PROMPT.strip() + "\n粉絲：" + user_text.strip()
    stream = chat.send_message_stream(message=prompt)
    full_reply = ""
    for chunk in stream:
        if chunk.text:
            print(chunk.text, end="", flush=True)
            full_reply += chunk.text
    print()
    return full_reply

# === 2. 切句函式 ===
def split_sentences(text: str) -> list[str]:
    return re.findall(r'[^。！？\n]+[。！？\n]?', text)

# === 3. Public Voice API（max 聲音） ===
PV_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGllbnRfaWQiOiJhd3NfaGFja2F0aG9uIiwiZXhwaXJlcyI6MTc0NTc0ODAwMH0.9qpg1xraE_d_Hua2brAmCfRlQSce6p2kdipgq8j1iqo"
API_URL  = "https://persona-sound.data.gamania.com/api/v1/public/voice"

def synthesize_segment(text: str) -> AudioSegment:
    """
    以 mode=file 直接回傳音檔二進位，並轉成 AudioSegment
    """
    resp = requests.get(
        API_URL,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {PV_TOKEN}"
        },
        params={
            "text": text,
            "model_id": 2,          # max 聲音[1]
            "speaker_name": "max",  # max 角色[1]
            "speed_factor": 1.0,
            "mode": "file"          # 直接回傳二進位音檔[1]
        }
    )
    resp.raise_for_status()
    ct = resp.headers.get("Content-Type", "")
    if "audio" not in ct:
        raise RuntimeError(f"API 回傳非音訊：{ct}，body={resp.text}")
    # 由二進位建立 AudioSegment
    return AudioSegment.from_file(io.BytesIO(resp.content), format="mp3")

# === 4. 播放段落 ===
def play_segment(seg: AudioSegment):
    """
    播放單一 AudioSegment 段落
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        seg.export(tmp.name, format="wav")
    wave = sa.WaveObject.from_wave_file(tmp.name)
    play = wave.play()
    play.wait_done()
    os.remove(tmp.name)

# === 5. 輸出資料夾 ===
SAVE_DIR = r"C:\Users\ASUS\Desktop\awsha\Gemini\assets"
os.makedirs(SAVE_DIR, exist_ok=True)

# === 6. 主程式 ===
if __name__ == "__main__":
    print("=== FEniX MAX AI 互動（Public Voice API 分段即時播放）===")
    while True:
        user_input = input("\n粉絲：").strip()
        if user_input.lower() in ("q", "quit", "exit"):
            print("Bye～ 臒侍，下次見！")
            break
        if not user_input:
            continue

        # 1. 用 Gemini 生成回覆
        print("MAX：", end="", flush=True)
        full_reply = chat_and_stream(user_input)

        # 2. 切句、逐段合成、播放、累積
        segments = split_sentences(full_reply)
        combined = AudioSegment.empty()
        for idx, sentence in enumerate(segments, 1):
            if sentence.strip():
                print(f"[播放段落 {idx}/{len(segments)}]")
                try:
                    seg = synthesize_segment(sentence)
                    play_segment(seg)
                    combined += seg
                except Exception as e:
                    print(f"第{idx}段合成失敗：{e}")

        # 3. 輸出完整 MP3
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        final_mp3 = os.path.join(SAVE_DIR, f"reply_max_{ts}.mp3")
        combined.export(final_mp3, format="mp3")
        print(f"完成：已儲存完整語音 {final_mp3}")
