import json

import PIL
from app import app
from flask import Response, request, send_file
from app.color import generate_collage
from app.utils import allowed_file, flat_extract, pil_image_to_bytes, is_safe_path, JSON_TYPE
from werkzeug.utils import secure_filename
import tempfile
import os


@app.post('/api/v1/collage')
def create_collage():
    request_file = request.files['file']
    collage_baseline_image = request.form['collage_image']

    if 'file' not in request.files:
        return Response(json.dumps({'status': 'no file in request'}), status=400, mimetype=JSON_TYPE)
    if request_file.filename == '':
        return Response(json.dumps({'status': 'empty file in request'}), status=400, mimetype=JSON_TYPE)
    if collage_baseline_image == '':
        return Response(json.dumps({'status': 'empty collage file in request'}), status=400, mimetype=JSON_TYPE)
    if not is_safe_path(os.getcwd(), collage_baseline_image):
        return Response(json.dumps({'status': 'collage file is invalid'}), status=400, mimetype=JSON_TYPE)

    if request_file and allowed_file(request_file.filename):
        upload_folder = tempfile.TemporaryDirectory()
        try:
            filename = secure_filename(request_file.filename)
            request_file.save(os.path.join(str(upload_folder.name), filename))
            files = flat_extract(filename, upload_folder.name)

            if files == 0:
                return Response(json.dumps({'status': 'Provided file does not contain any images'}), status=400, mimetype=JSON_TYPE)
            if not os.path.isfile(os.path.join(upload_folder.name, collage_baseline_image)):
                return Response(json.dumps({'status': 'collage file is not within provided files'}), status=400, mimetype=JSON_TYPE)

            try:
                collage_image = generate_collage(str(upload_folder.name), os.path.join(
                    str(upload_folder.name), collage_baseline_image))
                return send_file(pil_image_to_bytes(collage_image), mimetype='image/jpeg')
            except PIL.Image.DecompressionBombError:
                return Response(json.dumps({'status': 'one or more images are too large'}), status=400, mimetype=JSON_TYPE)
        finally:
            upload_folder.cleanup()
    return Response(json.dumps({'status': 'One or more errors occured during processing'}), status=400, mimetype=JSON_TYPE)


@app.get('/api/v1/collage')
def show_default_page():
    return Response(json.dumps({'status': 'invalid request'}), status=400, mimetype=JSON_TYPE)
