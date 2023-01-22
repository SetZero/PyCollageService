from io import BytesIO
import json

import PIL
from app import app
from flask import Response, flash, redirect, request, send_file
from app.color import generate_collage, MAPPING_IMAGE, INPUT_IMAGES
from flask_caching import Cache
from werkzeug.utils import secure_filename
import zipfile
import tempfile
import os
import shutil

ALLOWED_EXTENSIONS = set(['zip'])

cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
cache.init_app(app)

def allowed_file(filename):
    return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def flat_extract(filename, folder):
    my_zip = os.path.join(str(folder), filename)
    with zipfile.ZipFile(my_zip) as zip_file:
        for member in zip_file.namelist():
            filename = os.path.basename(member)
            # skip directories
            if not filename:
                continue

            # copy file (taken from zipfile's extract)
            source = zip_file.open(member)
            target = open(os.path.join(folder, filename), "wb")
            with source, target:
                shutil.copyfileobj(source, target)

def serve_pil_image(pil_img):
    img_io = BytesIO()
    pil_img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')

@app.post('/api/v1/collage')
def create_collage():
    if 'file' not in request.files:
        return Response(json.dumps({'status': 'no file in request'}), status=401, mimetype='application/json')

    request_file = request.files['file']
    if request_file.filename == '':
        return Response(json.dumps({'status': 'empty file in request'}), status=401, mimetype='application/json')
    if request_file and allowed_file(request_file.filename):
        upload_folder = tempfile.TemporaryDirectory()
        try:
            filename = secure_filename(request_file.filename)
            request_file.save(os.path.join(str(upload_folder.name), filename))
            flat_extract(filename, upload_folder.name)

            file_list = [f for f in os.listdir(str(upload_folder.name)) if os.path.isfile(os.path.join(str(upload_folder.name), f))]
            try:
                collage_image = generate_collage(str(upload_folder.name), os.path.join(str(upload_folder.name), file_list[1]))
                return serve_pil_image(collage_image)
            except  PIL.Image.DecompressionBombError:
                return Response(json.dumps({'status': 'one or more images are too large'}), status=401, mimetype='application/json')
        finally:
            upload_folder.cleanup()
    return Response(json.dumps({'status': 'One or more errors occured during processing'}), status=401, mimetype='application/json')

@app.get('/api/v1/collage')
def show_default_page():
    return Response(json.dumps({'status': 'invalid request'}), status=401, mimetype='application/json')