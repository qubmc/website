from app.config import ALLOWED_EXTENSIONS
from werkzeug.utils import secure_filename
import os
from app import app


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_file(request):
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return None
        file = request.files['file']
        # if user does not select file, browser also submits
        # an empty part without filename
        if file.filename == '':
            return None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],
                                   filename))
            return file.filename
    return None
