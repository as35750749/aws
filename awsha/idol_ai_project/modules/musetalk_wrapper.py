import subprocess

MUSETALK_DIR = r"C:\Users\ASUS\Desktop\aws game\MuseTalk"  # 改成你 MuseTalk 的實際路徑

def animate(audio_path: str, image_path: str, out_path: str):
    cmd = [
        "python", f"{MUSETALK_DIR}\\inference.py",
        "--input_audio", audio_path,
        "--input_image", image_path,
        "--output_path", out_path
    ]
    subprocess.run(cmd, check=True)
