import os
import yt_dlp

def download_YT():
    print("=== โปรแกรมดาวน์โหลด YouTube ===")
    url = input("กรุณาใส่ URL วิดีโอ YouTube: ").strip()
    
    if not url:
        print("❌ ลิงก์ไม่ถูกต้อง!")
        return

    print("\nเลือกรูปแบบที่ต้องการดาวน์โหลด:")
    print("1. ไฟล์เสียง MP3")
    print("2. ไฟล์วิดีโอ MP4")
    choice = input("กรอกหมายเลข (1 หรือ 2): ").strip()

    # กำหนดโฟลเดอร์ที่จะเซฟไฟล์ (สร้างโฟลเดอร์ downloads ให้อัตโนมัติ)
    save_path = os.path.join(os.getcwd(), "downloads")
    os.makedirs(save_path, exist_ok=True)
    outtmpl_pattern = os.path.join(save_path, "%(title)s.%(ext)s")

    if choice == "1":
        # ตั้งค่าสำหรับ MP3
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': outtmpl_pattern,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        media_type = "MP3"

    elif choice == "2":
        # ตั้งค่าสำหรับ MP4
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
            'outtmpl': outtmpl_pattern,
        }
        media_type = "MP4"

    else:
        print("❌ เลือกรูปแบบไม่ถูกต้อง!")
        return

    try:
        print(f"\nกำลังดาวน์โหลดไฟล์ {media_type}...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"\n✅ ดาวน์โหลดสำเร็จ!")
        print(f"📁 บันทึกไฟล์ไว้ที่โฟลเดอร์: {save_path}")

    except Exception as e:
        print(f"\n❌ เกิดข้อผิดพลาด: {e}")
while True:
    if __name__ == "__main__":
        download_YT()
    while True:
        answer = input("\nคุณต้องการดาวน์โหลดอีกครั้งหรือไม่? (y/n): ").strip().lower()
        if answer in ("y", "n"):
            break
        print("❌ กรุณาตอบ y หรือ n")

    if answer == "n":
        break