import os
from flask import Flask, render_template, request, jsonify, send_file
import yt_dlp

app = Flask(__name__)
DOWNLOAD_FOLDER = 'downloads'

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url')
    format_type = data.get('format', 'mp3')

    if not url:
        return jsonify({'error': 'กรุณากรอก URL'}), 400

    # 📌 วาง ydl_opts ตรงนี้ (ก่อนเรียกใช้ yt_dlp.YoutubeDL)
    ydl_opts = {
        # ปรับการเลือกฟอร์แมตให้ดึงเสียง/วิดีโอแบบเสถียร
        'format': 'bestaudio[ext=m4a]/bestaudio/best' if format_type == 'mp3' else 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        'quiet': True,
        'no_warnings': True,
        
        # บังคับใช้ IPv4 (ช่วยหลีกเลี่ยงการโดนบล็อก IPv6 บน Cloud Server)
        'source_address': '0.0.0.0', 

        # ปรับ User-Agent ล่าสุด
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        
        # ใช้ player_client ล่าสุดที่ไม่ติด PO Token และข้ามข้อจำกัดของ YouTube
        'extractor_args': {
            'youtube': {
                'player_client': ['mweb', 'tv', 'ios'],
                'player_skip': ['webpage', 'configs']
            }
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        # ส่งไฟล์กลับไปให้ผู้ใช้ดาวน์โหลด
        return send_file(
            filename,
            as_attachment=True,
            download_name=os.path.basename(filename)
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)