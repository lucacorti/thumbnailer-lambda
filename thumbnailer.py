import base64, io
from flask import Flask, jsonify, request
from PIL import Image

app = Flask(__name__)

@app.route('/thumbnailer', methods=['POST'])
def thumbnailer():
    size = request.json.get('size')
    if not size:
        return jsonify({
            'error': 'Missing or invalid input image size (Int)'
        }), 400

    data = request.json.get('data')
    if not data:
        return jsonify({
            'error': 'Missing or invalid input image data (String)'
        }), 400

    try:
        image = base64.b64decode(data)
        image = Image.open(io.BytesIO(image))
    except (TypeError, IOError) as e:
        return jsonify({
            'error': 'Uploaded file is corrupt or invalid'
        }), 400

    (width, height) = image.size
    if width < size or height < size:
        return jsonify({
            'error': 'Image smaller than requested thumbnail size'
        }), 400

    image.thumbnail((size, size))
    thumbnail = io.BytesIO()
    image.save(thumbnail, format=image.format)

    return jsonify({
        'data': base64.b64encode(thumbnail.getvalue()),
        'size': size
    }), 200

# We only need this for local development.
if __name__ == '__main__':
    app.run()
