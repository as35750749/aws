# chat_stream_with_public_tts.py

import os
import sys
import time
import tempfile
from datetime import datetime

import boto3
import requests
from playsound import playsound

# 系統提示：保持不變
SYSTEM_PROMPT = """
你現在是李承隆，FEniX 的忙內兼主唱。
請以短句、慢熱但溫柔的語氣回應粉絲，偶爾帶點冷幽默或反差萌。
"""

# Public Voice API 參數
API_URL = "https://persona-sound.data.gamania.com/api/v1/public/voice"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGllbnRfaWQiOiJhd3NfaGNrYWh0aG9uIiwiZXhwaXJlcyI6MTc0NTc0ODAwMH0.9qpg1xraE_d_Hua2brAmCfRlQSce6p2kdipgq8j1iqo"

def chat_and_stream(user_text: str) -> str:
    """呼叫 AWS Bedrock 的 Claude 3.7-sonnet 流式聊天"""
    client = boto3.client("bedrock-runtime", region_name="us-west-2")
    stream = client.converse_stream(
        modelId="anthropic.claude-3-7-sonnet-20250219-v1:0",
        system=[{"text": SYSTEM_PROMPT.strip()}],
        messages=[{"role": "user", "content": [{"text": user_text}]}],
        inferenceConfig={"maxTokens": 256, "temperature": 0.8, "topP": 0.9}
    )
    full_reply = ""
    print("李承隆：", end="", flush=True)
    for chunk in stream["stream"]:
        if "contentBlockDelta" in chunk:
            delta = chunk["contentBlockDelta"]["delta"]
            text = delta.get("text", "")
            print(text, end="", flush=True)
            full_reply += text
    print()  # 換行
    return full_reply

def tts_play_public(text: str, save_dir: str) -> str | None:
    """用 Public Voice API 合成語音，播放後可選擇儲存"""
    params = {
        "text": text,
        "model_id": 2,
        "speaker_name": "max",
        "speed_factor": 0.9,
        "mode": "file"
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {TOKEN}"
    }
    # 呼叫 API
    resp = requests.get(API_URL, headers=headers, json=params)
    if resp.status_code != 200 or "audio" not in resp.headers.get("Content-Type",""):
        print(f"❌ 語音 API 錯誤：{resp.status_code} {resp.text}")
        return None

    # 寫入暫存 wav 檔
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpf:
        tmpf.write(resp.content)
        tmp_path = tmpf.name

    try:
        print("▶️ 播放合成語音…")
        playsound(tmp_path)
        choice = input("播放結束，按 q 並 Enter 儲存，其他鍵放棄：").strip().lower()
        if choice == "q":
            os.makedirs(save_dir, exist_ok=True)
            out_path = os.path.join(save_dir, f"reply_{datetime.now():%Y%m%d_%H%M%S}.wav")
            with open(out_path, "wb") as f:
                f.write(resp.content)
            print(f"✅ 已儲存：{out_path}")
            return out_path
        else:
            print("已取消儲存。")
            return None
    finally:
        os.remove(tmp_path)

def main():
    save_dir = r"C:\Users\ASUS\Desktop\awsha\bedrockgtts\assets"
    print("=== FEniX 李承隆 AI 偶像互動 ===")
    print("輸入粉絲留言 (輸入 q 退出)：")

    while True:
        user_input = input("\n粉絲：").strip()
        if user_input.lower() in ("q", "quit", "exit"):
            print("Bye~ 小隆包，下次見！")
            break
        if not user_input:
            continue

        try:
            # 1. 串流聊天
            reply = chat_and_stream(user_input)
            # 2. 語音合成並播放
            tts_play_public(reply, save_dir)
        except KeyboardInterrupt:
            print("\n偵測到中斷，程式結束。")
            break
        except Exception as e:
            print(f"❗ 發生錯誤：{e}\n5秒後重試…")
            time.sleep(5)

if __name__ == "__main__":
    main()
