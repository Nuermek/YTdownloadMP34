import os
from urllib.parse import quote
from flask import Flask, render_template, request, send_file, jsonify
import yt_dlp

app = Flask(__name__)

DOWNLOAD_FOLDER = os.path.join(os.getcwd(), 'downloads')
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    url = data.get('url')
    format_type = data.get('format')

    if not url:
        return jsonify({'error': 'กรุณาใส่ URL'}), 400

    outtmpl = os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s')

    if format_type == 'mp3':
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': outtmpl,
            'windowsfilenames': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
    else:
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'merge_output_format': 'mp4',
            'outtmpl': outtmpl,
            'windowsfilenames': True,
        }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            if format_type == 'mp3':
                filename = os.path.splitext(filename)[0] + '.mp3'

        download_name = os.path.basename(filename)

        def generate_and_clean():
            with open(filename, 'rb') as f:
                while chunk := f.read(4096 * 1024):
                    yield chunk
            
            try:
                if os.path.exists(filename):
                    os.remove(filename)
            except Exception as e:
                print(f"เกิดข้อผิดพลาดในการลบไฟล์: {e}")

        response = app.response_class(
            generate_and_clean(),
            mimetype='application/octet-stream'
        )

        # ส่ง Header ทั้งแบบปกติและแบบ encoded ภาษาไทย
        response.headers["Access-Control-Expose-Headers"] = "X-Filename"
        response.headers["X-Filename"] = quote(download_name)

        return response

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)