import os
from flask import Flask, render_template, request, jsonify, send_file, after_this_request
import yt_dlp

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_FOLDER = os.path.join(BASE_DIR, 'downloads')
COOKIE_PATH = os.path.join(BASE_DIR, 'cookies.txt')

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

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

        if not os.path.exists(DOWNLOAD_FOLDER):
            os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

        if format_type == 'mp3':
            format_spec = 'ba/ba*/bestaudio/best'
        else:
            format_spec = 'bv*+ba/b/best'

        ydl_opts = {
            'format': format_spec,
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            'restrictfilenames': True,
            'quiet': True,
            'no_warnings': True,
            'source_address': '0.0.0.0',
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            # 📌 สลับใช้ Player Client ของ iOS / Android เพื่อ bypass HTTP 403 Forbidden
            'extractor_args': {
                'youtube': {
                    'player_client': ['ios', 'android', 'mweb']
                }
            }
        }

        if os.path.exists(COOKIE_PATH):
            ydl_opts['cookiefile'] = COOKIE_PATH

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        @after_this_request
        def remove_file(response):
            try:
                if os.path.exists(filename):
                    os.remove(filename)
            except Exception as e:
                app.logger.error(f"Error removing file: {e}")
            return response

        return send_file(
            filename,
            as_attachment=True,
            download_name=os.path.basename(filename)
        )

    except Exception as e:
        return jsonify({'error': f'ไม่สามารถดาวน์โหลดได้: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)