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
        'format': 'bestaudio/best' if format_type == 'mp3' else 'best',
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        'quiet': True,
        'no_warnings': True,
        
        # บังคับใช้ IPv4 ช่วยลดอัตราการโดนบล็อก IP บน Cloud
        'source_address': '0.0.0.0', 
        
        # ใช้ User-Agent ของอุปกรณ์พกพา
        'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
        
        # สลับมาใช้ client 'ios' หรือ 'mweb' ซึ่งมีโอกาสผ่านระบบตรวจจับสูงกว่า
        'extractor_args': {
            'youtube': {
                'player_client': ['ios', 'mweb']
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