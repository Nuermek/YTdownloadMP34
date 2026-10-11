import os
import shutil
from flask import Flask, render_template, request, jsonify, send_file, after_this_request
import yt_dlp

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_FOLDER = os.path.join(BASE_DIR, 'downloads')

# พาธต้นทางของ Secret File บน Render และ Local
RENDER_COOKIE_PATH = '/etc/secrets/cookies.txt'
LOCAL_COOKIE_PATH = os.path.join(BASE_DIR, 'cookies.txt')

# กำหนดโฟลเดอร์ชั่วคราวสำหรับคุกกี้ที่สามารถเขียน/อ่านได้
TEMP_COOKIE_PATH = os.path.join(DOWNLOAD_FOLDER, 'working_cookies.txt')

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def get_usable_cookie_path():
    """คัดลอกคุกกี้มาไว้ในโฟลเดอร์ที่เขียนไฟล์ได้เพื่อป้องกัน Read-only error"""
    source_cookie = None
    if os.path.exists(RENDER_COOKIE_PATH):
        source_cookie = RENDER_COOKIE_PATH
    elif os.path.exists(LOCAL_COOKIE_PATH):
        source_cookie = LOCAL_COOKIE_PATH

    if source_cookie:
        try:
            shutil.copyfile(source_cookie, TEMP_COOKIE_PATH)
            return TEMP_COOKIE_PATH
        except Exception as e:
            app.logger.error(f"Error copying cookie file: {e}")
            return source_cookie
    return None

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
            format_spec = 'best[ext=mp4]/best/bestvideo+bestaudio'

        ydl_opts = {
            'format': format_spec,
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            'restrictfilenames': True,
            'quiet': True,
            'no_warnings': True,
            'source_address': '0.0.0.0',
            'extractor_args': {
                'youtube': {
                    'player_client': ['web', 'default']
                }
            }
        }

        # ดึงพาธคุกกี้ชั่วคราวมาใช้งาน
        active_cookie = get_usable_cookie_path()
        if active_cookie:
            ydl_opts['cookiefile'] = active_cookie

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        @after_this_request
        def remove_file(response):
            try:
                if os.path.exists(filename):
                    # ปิดการลบทันทีบน Windows ชั่วคราว หรือปล่อยให้ยกเว้น Error 32
                    os.remove(filename)
            except Exception as e:
                # ถ้าติดปัญหาไฟล์กำลังถูกใช้งานอยู่บน Windows ให้ข้ามไปก่อน ไม่ต้องแสดง Log Error พลาด
                pass
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