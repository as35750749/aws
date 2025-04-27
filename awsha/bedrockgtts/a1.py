from google import genai

client = genai.Client(api_key="AIzaSyBm5DB9zryMyQyqFJc5icl3u9uKAxDBHQM")

try:
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents="測試金鑰有效性"
    )
    print("金鑰有效！回應內容：", response.text)
except Exception as e:
    print("金鑰無效，錯誤訊息：", str(e))
