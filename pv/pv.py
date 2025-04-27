import requests
import os
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

API_URL = "https://persona-sound.data.gamania.com/api/v1/public/voice"
TOKEN   = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGllbnRfaWQiOiJhd3NfaGFja2F0aG9uIiwiZXhwaXJlcyI6MTc0NTc0ODAwMH0.9qpg1xraE_d_Hua2brAmCfRlQSce6p2kdipgq8j1iqo"

# 1. 建立 Session 並設定重試策略、關閉 Keep-Alive
session = requests.Session()
retry_strategy = Retry(total=5, backoff_factor=0.5, status_forcelist=[500,502,503,504])
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("https://", adapter)
session.mount("http://", adapter)

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Connection": "close",
}

params = {
    "text":         "大家好，    、、、我是MAX，  、、      在這邊提前祝各位黑客松比賽順利，、、、、、、、、、、、、掰拉 、、",
    "model_id":     2,
    "speaker_name": "max",
    "speed_factor": 0.9,
    "mode":         "file",
}

# 2. 呼叫 Public Voice API 拿 media_url
resp = session.get(API_URL, headers=headers, params=params, timeout=10)
if resp.status_code == 403:
    err = resp.json().get("message", resp.text)
    print("❌ Token 驗證失敗：", err)
    exit(1)
if resp.status_code != 200 or not resp.headers.get("Content-Type","").startswith("application/json"):
    print("❌ API 回傳非預期格式：", resp.text)
    exit(1)

media_url = resp.json().get("media_url")
if not media_url:
    print("❌ 未取得 media_url，回傳內容：", resp.json())
    exit(1)
print("取得音檔網址：", media_url)

# 3. 下載並另存 mp3 檔
out_path = "self_intro.mp3"
with session.get(media_url, headers={"User-Agent":"Mozilla/5.0"}, stream=True, timeout=10) as r:
    if r.status_code != 200:
        print("❌ 下載音檔失敗：", r.status_code)
        exit(1)
    with open(out_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

print("✅ 已儲存音檔：", os.path.abspath(out_path))
