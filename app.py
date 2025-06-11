from flask import Flask, request, render_template
import subprocess
import json
import os

app = Flask(__name__)

EXIF_TOOLS_PATH = 'C:\Tools\ExifViewers\exiftool-13.30_64\exiftool.exe'

TEMP_DIR = os.path.join(os.path.dirname(__file__), 'temp')
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

def is_json(content):
    try:
        json.loads(content)
        return True
    except ValueError:
        return False

def format_json(content):
    try:
        json_data = json.loads(content)
        return json.dumps(json_data, indent=4)
    except ValueError:
        return content

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'image_file' in request.files:
            image_file = request.files['image_file']
            file_path = os.path.join(TEMP_DIR, image_file.filename)
            image_file.save(file_path)
            try:
                output = subprocess.check_output([EXIF_TOOLS_PATH, file_path]).decode('utf-8')
                exif_data = {}
                for line in output.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip()
                        value = value.strip()
                        if is_json(value):
                            value = format_json(value)
                        exif_data[key] = value
                return render_template('exif.html', exif_data=exif_data)
            except Exception as e:
                return str(e)
        else:
            return "No file uploaded."
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)