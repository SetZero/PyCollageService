import json

import PIL
from app import app
from flask import Response, flash, redirect, request, send_file
from app.color import generate_collage, MAPPING_IMAGE, INPUT_IMAGES
from app.utils import allowed_file, flat_extract, pil_image_to_bytes
from werkzeug.utils import secure_filename
import tempfile
import os


@app.post('/api/v1/collage')
def create_collage():
    if 'file' not in request.files:
        return Response(json.dumps({'status': 'no file in request'}), status=401, mimetype='application/json')

    request_file = request.files['file']
    if request_file.filename == '':
        return Response(json.dumps({'status': 'empty file in request'}), status=401, mimetype='application/json')
    if request.form['collage_image'] == '':
        return Response(json.dumps({'status': 'empty collage file in request'}), status=401, mimetype='application/json')

    if request_file and allowed_file(request_file.filename):
        upload_folder = tempfile.TemporaryDirectory()
        try:
            filename = secure_filename(request_file.filename)
            request_file.save(os.path.join(str(upload_folder.name), filename))
            flat_extract(filename, upload_folder.name)

            try:
                collage_image = generate_collage(str(upload_folder.name), os.path.join(str(upload_folder.name), request.form['collage_image']))
                return send_file(pil_image_to_bytes(collage_image), mimetype='image/jpeg')
            except  PIL.Image.DecompressionBombError:
                return Response(json.dumps({'status': 'one or more images are too large'}), status=401, mimetype='application/json')
        finally:
            upload_folder.cleanup()
    return Response(json.dumps({'status': 'One or more errors occured during processing'}), status=401, mimetype='application/json')

@app.get('/api/v1/collage')
def show_default_page():
    return Response(json.dumps({'status': 'invalid request'}), status=401, mimetype='application/json')