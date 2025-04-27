import os
import replicate

# 1. 設定你的 API 金鑰（一定要在 import replicate 之後立刻設定）
os.environ["REPLICATE_API_TOKEN"] = "r8_WyvIVsSfz9hK1nHxFeaqZJql3xF0WDX1Iioz0"
# 或者：replicate.api_token = "r8_WyvIVsSfz9hK1nHxFeaqZJql3xF0WDX1Iioz0"

# 2. 先取得模型並列出可用的版本 ID
model = replicate.models.get("douwantech/musev")
versions = model.versions.list()
print("Available version IDs:")
for v in versions:
    print("  ", v.id)

# 3. 選一個版本（通常用列表的第一個就是最新）
version_id = versions[0].id
print("Using version:", version_id)

# 4. 呼叫推理（注意：必須帶上版本號）
output = replicate.run(
    f"douwantech/musev:{version_id}",
    input={
        # 圖片用 open(...,"rb") 上傳
        "image_input": open(r"C:\Users\ASUS\Desktop\max.jpg", "rb"),
        # 如果要唇形同步，再加一行：
        # "audio_input": open(r"C:\Users\ASUS\Desktop\111.wav", "rb"),
        "fps": 30,               # 可選，控制影片幀率
    }
)

# 5. 將結果寫到本地檔案
with open("output.mp4", "wb") as f:
    f.write(output.read())
print("Done: output.mp4 寫入完畢")
