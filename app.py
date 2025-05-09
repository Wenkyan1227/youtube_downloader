import os
import openpyxl
import subprocess
import glob
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Define folders and filenames
DOWNLOAD_FOLDER = 'downloads'
AUDIO_FOLDER = 'audios'
UPLOAD_FOLDER = 'uploads'
EXCEL_FILENAME = 'youtube_links.xlsx'

def download_media(url, mode):
    folder = DOWNLOAD_FOLDER if mode == 'video' else AUDIO_FOLDER
    os.makedirs(folder, exist_ok=True)

    # Use yt-dlp to download the file
    output_template = os.path.join(folder, '%(title)s.%(ext)s')
    if mode == 'video':
        command = ['yt-dlp', '-o', output_template, url]
    else:  # audio
        command = ['yt-dlp', '--format', 'bestaudio', '-o', output_template, url]

    try:
        subprocess.run(command, check=True)

        # Get most recent file in folder (assumes it’s the one just downloaded)
        list_of_files = glob.glob(os.path.join(folder, '*'))
        latest_file = max(list_of_files, key=os.path.getctime)
        return True, latest_file
    except subprocess.CalledProcessError:
        return False, url

def convert_audio_to_mp3(file_path):
    try:
        base, _ = os.path.splitext(file_path)
        mp3_path = base + ".mp3"

        command = ['ffmpeg', '-y', '-i', file_path, '-vn', '-ar', '44100', '-ac', '2', '-b:a', '192k', mp3_path]
        subprocess.run(command, check=True)

        # Delete the original .webm or other input file after successful conversion
        if os.path.exists(mp3_path):
            os.remove(file_path)

        return mp3_path
    except subprocess.CalledProcessError as e:
        return f"FFmpeg conversion failed: {e}"

def process_excel_and_download(mode):
    file_path = os.path.join(UPLOAD_FOLDER, EXCEL_FILENAME)
    if not os.path.exists(file_path):
        return {'message': 'Excel file not found.', 'status': 'error'}

    try:
        wb = openpyxl.load_workbook(file_path)
        sheet = wb.active
        links = [str(row[0].value) for row in sheet.iter_rows(min_row=2, min_col=1, max_col=1) if row[0].value and str(row[0].value).startswith("http")]

        if not links:
            return {'message': 'No valid URLs found in Excel file.', 'status': 'error'}

        folder = DOWNLOAD_FOLDER if mode == 'video' else AUDIO_FOLDER
        existing_files = set(os.listdir(folder))

        failed = []
        for url in links:
            success, file_path = download_media(url, mode)
            if not success:
                failed.append(file_path)
            elif mode == 'audio':
                mp3_path = convert_audio_to_mp3(file_path)
                if not os.path.exists(mp3_path):
                    failed.append(url)

        all_files = set(os.listdir(folder))
        new_files = list(all_files - existing_files)

        return {
            'status': 'success',
            'message': f'{len(new_files)} {mode} file(s) downloaded.',
            'files': new_files,
            'failed': failed
        }

    except Exception as e:
        return {'message': str(e), 'status': 'error'}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download_excel_video', methods=['POST'])
def download_excel_video():
    return jsonify(process_excel_and_download(mode='video'))

@app.route('/download_excel_audio', methods=['POST'])
def download_excel_audio():
    return jsonify(process_excel_and_download(mode='audio'))

@app.route('/download_video', methods=['POST'])
def download_single_video():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'message': 'URL is required.', 'status': 'error'})

    folder = DOWNLOAD_FOLDER
    os.makedirs(folder, exist_ok=True)
    existing_files = set(os.listdir(folder))

    success, _ = download_media(url, mode='video')
    if not success:
        return jsonify({'message': 'Failed to download video.', 'status': 'error'})

    all_files = set(os.listdir(folder))
    new_files = list(all_files - existing_files)

    return jsonify({
        'message': 'Video downloaded successfully.',
        'status': 'success',
        'files': new_files
    })

@app.route('/download_audio', methods=['POST'])
def download_single_audio():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'message': 'URL is required.', 'status': 'error'})

    folder = AUDIO_FOLDER
    os.makedirs(folder, exist_ok=True)
    existing_files = set(os.listdir(folder))

    success, file_path = download_media(url, mode='audio')
    if not success:
        return jsonify({'message': 'Failed to download audio.', 'status': 'error'})

    # Convert audio to MP3
    converted_path = convert_audio_to_mp3(file_path)
    if not os.path.exists(converted_path):
        return jsonify({'message': converted_path, 'status': 'error'})

    all_files = set(os.listdir(folder))
    new_files = list(all_files - existing_files)

    return jsonify({
        'message': 'Audio downloaded and converted successfully.',
        'status': 'success',
        'converted_file': os.path.basename(converted_path),
        'files': new_files
    })

if __name__ == '__main__':
    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
    os.makedirs(AUDIO_FOLDER, exist_ok=True)
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
