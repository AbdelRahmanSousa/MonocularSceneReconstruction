import os

path = r'C:\Users\Abdel\Projects\FCIS\monocular_3d_scene_reconstruction_for_real_world_modeling\uploaded\images'

count = 0
for i in os.listdir(path):
    if i.__contains__(' '):
        os.remove(os.path.join(path, i))
    #os.rename(os.path.join(path, i), os.path.join(path, i.replace(' ', '_')))
    # count = count + 1
    # file_parts = i.split('.')
    # ext = ''
    # if len(file_parts) > 1:
    #     ext = file_parts[-1]
    # os.rename(os.path.join(path, i), os.path.join(path, f'{count}.{ext}'))