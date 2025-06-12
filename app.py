from flask import Flask, request, render_template
import subprocess
import json
import os
import tempfile
import platform
import re


app = Flask(__name__)

if platform.system() == 'Windows':
    EXIF_TOOLS_PATH = 'C:\\Tools\\ExifViewers\\exiftool-13.30_64\\exiftool.exe'
    USE_TEMPFILE = False
else:
    EXIF_TOOLS_PATH = 'exiftool'
    USE_TEMPFILE = True

def is_json(content):
    if not content:
        return False
    try:
        parsed = json.loads(content)
        # Check if the parsed content is a dictionary or list
        return isinstance(parsed, (dict, list))
    except Exception:
        return False

def format_json(content):
    try:
        json_data = json.loads(content)
        pretty_json = json.dumps(json_data, indent=2)
        # Add basic syntax highlighting
        pretty_html = re.sub(r'"(.*?)":', r'<span style="color: #69ff70;">"\1":</span>', pretty_json)
        pretty_html = pretty_html.replace('{', '<span style="color: #66d9ef;">{</span>')
        pretty_html = pretty_html.replace('}', '<span style="color: #66d9ef;">}</span>')
        pretty_html = pretty_html.replace('[', '<span style="color: #a6e22e;">[</span>')
        pretty_html = pretty_html.replace(']', '<span style="color: #a6e22e;">]</span>')
        pretty_html = pretty_html.replace(',', '<span style="color: #bbbbbb;">,</span>')
        return pretty_html
    except ValueError:
        return content
    
# Register the filters with Flask's Jinja environment
app.jinja_env.filters['is_json'] = is_json
app.jinja_env.filters['format_json'] = format_json

def process_exif_data(file_path):
    try:
        output = subprocess.check_output([EXIF_TOOLS_PATH, file_path]).decode('utf-8')
        exif_data = {}
        for line in output.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                exif_data[key] = value
        return render_template('exif.html', exif_data=exif_data)
    except Exception as e:
        return str(e)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'image_file' in request.files:
            TEMP_DIR = os.path.join(os.path.dirname(__file__), 'temp')
            if not os.path.exists(TEMP_DIR):
                os.makedirs(TEMP_DIR)

            image_file = request.files['image_file']
            if USE_TEMPFILE:
                with tempfile.NamedTemporaryFile(delete=True, dir=TEMP_DIR) as temp_file:
                    file_path = temp_file.name
                    print(f"Temporary file created at: {file_path}")
                    image_file.save(file_path)
                    return process_exif_data(file_path)
            else:
                file_path = os.path.join(TEMP_DIR, 'temp_image.jpg')
                print(f"Temporary file created at: {file_path}")
                image_file.save(file_path)
                return process_exif_data(file_path)
        else:
            return "No file uploaded."
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)