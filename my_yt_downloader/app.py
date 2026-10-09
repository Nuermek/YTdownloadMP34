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
    try:
        data = request.get_json(silent=True)
        if not data or 'url' not in data:
            return jsonify({'error': 'กรุณากรอก URL ที่ถูกต้อง'}), 400

        url = data.get('url')
        format_type = data.get('format', 'mp3')

        ydl_opts = {
            'format': 'bestaudio/best' if format_type == 'mp3' else 'best',
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
            'source_address': '0.0.0.0',
            # ปรับแต่ง User-Agent ทั่วไป
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        return send_file(
            filename,
            as_attachment=True,
            download_name=os.path.basename(filename)
        )

    except Exception as e:
        # บังคับคืนค่า Error เป็น JSON 100% เสมอ
        return jsonify({'error': f'ไม่สามารถดาวน์โหลดได้: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)