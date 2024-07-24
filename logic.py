from camera_localization.colmap import ColMapLocalization, ColmapLocalizationPredictOptions
from camera_localization.hloc_model import HLOCModel, HLOCPredictOptions
from preprocessing_wizards import *
import cv2
import os
import time
from src.GLOBAL import GLOBAL
from model.instant_ngp import InstantNGPPredictOptions, InstantNGP

poseEstimators = {'colmap': (ColMapLocalization(), ColmapLocalizationPredictOptions('', '', '')),
                  'hloc': (HLOCModel(), HLOCPredictOptions('', '', ''))}
preprocessing_wizards = {'clahe': CLAHE(2.0, (8, 8)),
                         'filtering': Filtering(),
                         'augmentation': Augmentation(),
                         'white balancing': WhiteBalancing(),
                         'white_balancing': WhiteBalancing()}


def reconstruct(path: str, preprocessing_pipeline: list, model: str, pose_estimator: str):
    path = os.path.abspath(path)
    # Preprocess
    pipeline = [Resizing(high=2773, low=1560)]
    for i in preprocessing_pipeline:
        pipeline.append(preprocessing_wizards[i])
    imgs_path = os.path.join(path, 'images')
    tic_pp = time.perf_counter()
    for name in os.listdir(imgs_path):
        img = cv2.imread(os.path.join(imgs_path, name))
        p_img = PPWizard.run_pipeline(img, pipeline)
        cv2.imwrite(os.path.join(imgs_path, name), p_img[0])
    toc_pp = time.perf_counter()

    # Estimate Pose
    if pose_estimator not in poseEstimators:
        return
    tic_pe = time.perf_counter()
    pose_tuple = poseEstimators[pose_estimator]
    pose_tuple[1].path = path
    pose_tuple[1].images_folder = 'images'
    pose_tuple[1].output_path = os.path.join(path, 'transforms.json')
    pose_tuple[0].predict(pose_tuple[1])
    toc_pe = time.perf_counter()
    # Reconstruct
    if model == 'nerf':
        tic_rec = time.perf_counter()
        opts = InstantNGPPredictOptions(os.path.abspath(path), GLOBAL.instant_ngp, save_mesh='./Results/nerfmesh.obj',
                                        save_snapshot='./Results/nerfsnapshot.ingp', marching_cubes_res=512,
                                        marching_cubes_thresh=2.5)
        InstantNGP().predict(opts)
        toc_rec = time.perf_counter()
        print(f"Time for preprocessing: {toc_pp - tic_pp:0.4f}")
        print(f"Time for pose: {toc_pe - tic_pe:0.4f}")
        print(f"Time for reconstruction: {toc_rec - tic_rec:0.4f}")
    elif model == 'gtsfm':
        pass
    else:
        raise ValueError()


import json


def bytes_to_json_dict(data):
    """
  This function takes a byte array, a starting index, and an ending index (exclusive),
  extracts a chunk of bytes, converts them to a UTF-8 string, and attempts to parse it as a JSON dictionary.

  Args:
      data: The byte array containing the data.

  Returns:
      A Python dictionary representing the parsed JSON data, or None if parsing fails.

  Raises:
      ValueError: If the start or end index is out of bounds.
  """
    # Extract the chunk of bytes
    chunk = data

    # Try to decode the bytes as UTF-8 and parse as JSON
    try:
        json_string = chunk.decode('utf-8')
        return json.loads(json_string)
    except (UnicodeDecodeError, json.JSONDecodeError):
        # Handle potential decoding or parsing errors
        return None
