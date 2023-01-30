import shutil
import zipfile
from io import BytesIO
import os
from PIL import Image

import app

ALLOWED_EXTENSIONS = set(['zip'])
JSON_TYPE='application/json'


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def verify_image(image):
    with Image.open(image) as img:
        try:
            img.verify()
            return True
        except Exception:
            return False


def flat_extract(filename, folder):
    my_zip = os.path.join(str(folder), filename)
    with zipfile.ZipFile(my_zip) as zip_file:
        file_counter = 0
        for member in zip_file.namelist():
            filename = os.path.basename(member)
            # skip directories
            if not filename:
                continue

            # copy file (taken from zipfile's extract)
            try:
                source = zip_file.open(member)
                # if not verify_image(source):
                #    app.logger.info('%s is not an image', source)
                #    continue

                target = open(os.path.join(folder, filename), "wb")
                with source, target:
                    shutil.copyfileobj(source, target)
                    file_counter += 1
            except RuntimeError:
                continue
        return file_counter


def pil_image_to_bytes(pil_img, filetype='JPEG'):
    img_io = BytesIO()
    pil_img.save(img_io, filetype, quality=70)
    img_io.seek(0)
    return img_io


def is_safe_path(basedir, path, follow_symlinks=True):
    if follow_symlinks:
        matchpath = os.path.realpath(path)
    else:
        matchpath = os.path.abspath(path)
    return basedir == os.path.commonpath((basedir, matchpath))
