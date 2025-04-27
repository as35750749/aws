import subprocess

# 原始 MP3 路徑與輸出 WAV 檔名
input_file = r'C:\Users\ASUS\Desktop\pv\self_intro.mp3'
output_file = r'C:\Users\ASUS\Desktop\pv\self_intro_16k_mono.wav'

# ffmpeg 指令：-y 自動覆蓋，
# -i 輸入檔，
# -acodec pcm_s16le 指定輸出為 16-bit PCM，
# -ac 1 轉單聲道，
# -ar 16000 取樣率 16kHz[2]，
# 最後接輸出檔路徑
cmd = [
    'ffmpeg',
    '-y',
    '-i', input_file,
    '-acodec', 'pcm_s16le',
    '-ac', '1',
    '-ar', '16000',
    output_file
]

# 執行轉檔
subprocess.run(cmd, check=True)
print(f'✅ 已轉檔並儲存於：{output_file}')
