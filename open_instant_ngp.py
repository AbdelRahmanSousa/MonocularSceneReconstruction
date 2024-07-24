import sys
sys.path.append(r'C:\Users\Abdel\Projects\FCIS\monocular_3d_scene_reconstruction_for_real_world_modeling\instant-ngp\build')
from model.instant_ngp import *
from camera_localization.colmap import *
ColMapLocalization().predict(ColmapLocalizationPredictOptions('', '', ''))
input()