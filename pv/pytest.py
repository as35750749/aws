import requests
import tempfile, os, json
from playsound import playsound

API_URL = "https://persona-sound.data.gamania.com/api/v1/public/voice"
TOKEN   = "你的 Bearer TOKEN"

# 只帶 Authorization，其他交給 requests 預設
headers = {
    "Authorization": f"Bearer {TOKEN}"
}

payload = {
    "text": "五月十七日星期六，Mars!! Born!! Beyond!! 台北國際會議中心，不見不散！",
    "model_id":     2,
    "speaker_name": "max",
    "speed_factor": 0.9,
    "mode":         "file"
}

# 注意：這裡改用 data=json.dumps(...)，而把 Content-Type 留空
resp = requests.post(
    API_URL,
    headers=headers,
    data=json.dumps(payload).encode("utf-8")
)

print("狀態碼:", resp.status_code)
print("回傳 Content-Type:", resp.headers.get("Content-Type"))

if resp.status_code == 200 and resp.headers.get("Content-Type", "").startswith("audio/"):
    # 暫存成 mp3
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        tmp.write(resp.content)
        tmp_path = tmp.name

    try:
        print("播放音檔…")
        playsound(tmp_path)
        choice = input("按 q 儲存，其他鍵跳過：").strip().lower()
        if choice == "q":
            out_path = "self_intro.mp3"
            with open(out_path, "wb") as f:
                f.write(resp.content)
            print("已儲存到：", out_path)
        else:
            print("已取消儲存。")
    finally:
        os.remove(tmp_path)

else:
    # 若還是失敗，就印出 response.text
    print("API call 失敗，回傳內容：", resp.text)
