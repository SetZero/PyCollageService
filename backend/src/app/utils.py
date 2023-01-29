import shutil
import zipfile
from io import BytesIO
import os

ALLOWED_EXTENSIONS = set(['zip'])

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

def pil_image_to_bytes(pil_img, filetype='JPEG'):
    img_io = BytesIO()
    pil_img.save(img_io, filetype, quality=70)
    img_io.seek(0)
    return img_io