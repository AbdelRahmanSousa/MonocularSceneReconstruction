import json.decoder
import shutil

from flask import Blueprint, render_template, request, redirect, make_response, send_from_directory, send_file
from logic import *

import zipfile

core_bp = Blueprint("core", __name__)


@core_bp.route("/")
def home():
    return send_from_directory('./src/static', 'index.html')

@core_bp.route("/debug")
def debug():
    return render_template('core/nerf.html')

@core_bp.route("/start_nerf", methods=["POST"])
def start_nerf():
    try:
        # Start Instant ngp with the given estimatior
        if 'boundary' not in request.headers:
            return make_response(400)
        boundary = request.headers.get('boundary')
        json = bytes_to_json_dict(request.data[0: int(boundary)])
        pose_estimator = json["estimator"]
        preprocessing_methods = json['preprocessing']
        model = json['model']
        if not os.path.isdir('./uploaded'):
            os.mkdir('./uploaded')
        images = request.data[int(boundary):]
        with open('./uploaded/temp.zip', 'wb') as f:
            f.write(images)
            f.close()
        if zipfile.is_zipfile("./uploaded/temp.zip"):
            zipfile.ZipFile("./uploaded/temp.zip").extractall("./uploaded")
        reconstruct('./uploaded', preprocessing_methods, 'nerf', pose_estimator)
    except Exception as e:
        shutil.rmtree('./uploaded')
        return make_response(500)
    finally:
        shutil.rmtree('./uploaded')
    return send_file('./results/nerfsnapshot.ingp', as_attachment=True)

@core_bp.route("/start_nerf_debug", methods=["POST"])
def start_nerf_debug():
    try:
        # Start Instant ngp with the given estimatior
        pose_estimator = request.form["estimator"]
        preprocessing_methods = []
        for i in request.form.getlist('preprocessing'):
            preprocessing_methods.append(i)
        if not os.path.isdir('./uploaded'):
            os.mkdir('./uploaded')
        images = request.files['images']
        images.save('./uploaded/temp.zip')
        if zipfile.is_zipfile("./uploaded/temp.zip"):
            zipfile.ZipFile("./uploaded/temp.zip").extractall("./uploaded")
        reconstruct('./uploaded', preprocessing_methods, 'nerf', pose_estimator)
    except Exception as e:
        shutil.rmtree('./uploaded')
        return make_response(500)
    finally:
        shutil.rmtree('./uploaded')
    return redirect('/', 302)


