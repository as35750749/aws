import shutil

def synthesize(text: str, out_path: str):
    print(f"[模擬 Public Voice] 合成語音: {text}")
    # 用測試語音檔案代替合成結果
    shutil.copyfile("assets/test_idol.wav", out_path)
