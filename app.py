from flask import Flask, request, render_template
import subprocess
import json

app = Flask(__name__)

EXIF_TOOLS_PATH = 'C:\Tools\ExifViewers\exiftool-13.30_64\exiftool.exe'

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
        image_path = request.form['image_path']
        try:
            output = subprocess.check_output([EXIF_TOOLS_PATH, image_path]).decode('utf-8')
            print(output)
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
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)