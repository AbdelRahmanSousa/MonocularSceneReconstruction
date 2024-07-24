import argparse
import os
import commentjson as json
import sys


import numpy as np
import shutil
import time
import pyngp as ngp
from .common import *
from .scenes import *

from tqdm import tqdm


class InstantNGPPredictOptions:
    def __init__(self, training_data, root_dir, load_snapshot=None, save_snapshot=None, network_config_path=None, n_steps=-1, files="",
                 near_distance=-1, exposure=0.0, sharpening=0.0, save_mesh=".", marching_cubes_res=256,
                 marching_cubes_thresh=2.5, gui=True, width=1920, height=1080):
        """
        :param gui: whether to open gui or not
        :param width: width of gui window
        :param height: height of gui window
        :param load_snapshot: path to load snapshot from
        :param save_snapshot: path to save snapshot to
        :param network_config_path: path of the network config
        :param n_steps: number of steps before training stops
        :param files: Files to be loaded. Can be a scene, network config, snapshot, camera path, or a combination of those.
        :param training_data: The scene to load. Can be the scene's name or a full path to the training data. Can be NeRF dataset, a *.obj/*.stl mesh for training a SDF, an image, or a *.nvdb volume.
        :param exposure: Controls the brightness of the image. Positive numbers increase brightness, negative numbers decrease it.
        :param near_distance: Set the distance from the camera at which training rays start for nerf. <0 means use ngp default
        :param sharpening: Set amount of sharpening applied to NeRF training images. Range 0.0 to 1.0.
        :param save_mesh: Output a marching-cubes based mesh from the NeRF or SDF model. Supports OBJ and PLY format.
        :param marching_cubes_res: Sets the resolution for the marching cubes grid.
        :param marching_cubes_thresh: Sets the density threshold for marching cubes.
        """
        self.load_snapshot = load_snapshot
        self.save_snapshot = save_snapshot
        self.network_config_path = network_config_path
        self.n_steps = n_steps
        self.files = files
        self.root_dir = root_dir
        self.training_data = training_data
        self.near_distance = near_distance
        self.exposure = exposure
        self.sharpen = sharpening
        self.save_mesh = save_mesh
        self.marching_cubes_res = marching_cubes_res
        self.marchines_cubes_thresh = marching_cubes_thresh
        self.width = width
        self.height = height
        self.gui = gui


class InstantNGP:

    def get_scene(self, scene):
        for scenes in [scenes_sdf, scenes_nerf, scenes_image, scenes_volume]:
            if scene in scenes:
                return scenes[scene]
        return None

    def view_snapshot(self, root_dir, size:tuple, snapshot):
        testbed = ngp.Testbed()
        testbed.root_dir = root_dir

        # Pick a sensible GUI resolution depending on arguments.
        sw = size[0] or 1920
        sh = size[1] or 1080
        while sw * sh > 1920 * 1080 * 4:
            sw = int(sw / 2)
            sh = int(sh / 2)
        testbed.init_window(sw, sh, second_window=False)

        scene_info = self.get_scene(snapshot)
        if scene_info is not None:
            snapshot = default_snapshot_filename(scene_info)
        testbed.load_snapshot(snapshot)
        repl(testbed)

    def predict(self, opts: InstantNGPPredictOptions):
        testbed = ngp.Testbed()
        testbed.root_dir = opts.root_dir
        if opts.training_data:
            scene_info = self.get_scene(opts.training_data)
            if scene_info is not None:
                opts.scene = os.path.join(scene_info["data_dir"], scene_info["dataset"])
                if not opts.network and "network" in scene_info:
                    opts.network = scene_info["network"]

            testbed.load_training_data(opts.training_data)
        if opts.gui:
            # Pick a sensible GUI resolution depending on arguments.
            sw = opts.width or 1920
            sh = opts.height or 1080
            while sw * sh > 1920 * 1080 * 4:
                sw = int(sw / 2)
                sh = int(sh / 2)
            testbed.init_window(sw, sh, second_window=False)


        if opts.load_snapshot is not None:
            scene_info = self.get_scene(opts.load_snapshot)
            if scene_info is not None:
                opts.load_snapshot = default_snapshot_filename(scene_info)
            testbed.load_snapshot(opts.load_snapshot)
        elif opts.network_config_path is not None:
            testbed.reload_network_from_file(opts.network_config_path)

        if testbed.mode == ngp.TestbedMode.Sdf:
            testbed.tonemap_curve = ngp.TonemapCurve.ACES

        testbed.nerf.sharpen = float(opts.sharpen)
        testbed.exposure = opts.exposure
        testbed.shall_train = True
        testbed.nerf.render_with_lens_distortion = True

        network_stem = os.path.splitext(os.path.basename(opts.network_config_path))[0] if opts.network_config_path else "base"
        if testbed.mode == ngp.TestbedMode.Sdf:
            setup_colored_sdf(testbed, opts.scene)

        if opts.near_distance >= 0.0:
            print("NeRF training ray near_distance ", opts.near_distance)
            testbed.nerf.training.near_distance = opts.near_distance


            # Prior nerf papers accumulate/blend in the sRGB
            # color space. This messes not only with background
            # alpha, but also with DOF effects and the likes.
            # We support this behavior, but we only enable it
            # for the case of synthetic nerf data where we need
            # to compare PSNR numbers to results of prior work.
            testbed.color_space = ngp.ColorSpace.SRGB

            # No exponential cone tracing. Slightly increases
            # quality at the cost of speed. This is done by
            # default on scenes with AABB 1 (like the synthetic
            # ones), but not on larger scenes. So force the
            # setting here.
            testbed.nerf.cone_angle_constant = 0

            # Match nerf paper behaviour and train on a fixed bg.
            testbed.nerf.training.random_bg_color = False

        old_training_step = 0
        n_steps = opts.n_steps

        # If we loaded a snapshot, didn't specify a number of steps, _and_ didn't open a GUI,
        # don't train by default and instead assume that the goal is to render screenshots,
        # compute PSNR, or render a video.
        if n_steps < 0 and (not opts.load_snapshot or opts.gui):
            n_steps = 150000

        tqdm_last_update = 0
        if n_steps > 0:
            with tqdm(desc="Training", total=n_steps, unit="steps") as t:
                while testbed.frame():
                    if testbed.want_repl():
                        repl(testbed)
                    # What will happen when training is done?
                    if testbed.training_step >= n_steps:
                        if opts.gui:
                            testbed.shall_train = False
                        else:
                            break

                    # Update progress bar
                    if testbed.training_step < old_training_step or old_training_step == 0:
                        old_training_step = 0
                        t.reset()

                    now = time.monotonic()
                    if now - tqdm_last_update > 0.1:
                        t.update(testbed.training_step - old_training_step)
                        t.set_postfix(loss=testbed.loss)
                        old_training_step = testbed.training_step
                        tqdm_last_update = now

        if opts.save_snapshot:
            os.makedirs(os.path.dirname(opts.save_snapshot), exist_ok=True)
            testbed.save_snapshot(opts.save_snapshot, False)

        # if opts.test_transforms:
        #     print("Evaluating test transforms from ", opts.test_transforms)
        #     with open(opts.test_transforms) as f:
        #         test_transforms = json.load(f)
        #     data_dir = os.path.dirname(opts.test_transforms)
        #     totmse = 0
        #     totpsnr = 0
        #     totssim = 0
        #     totcount = 0
        #     minpsnr = 1000
        #     maxpsnr = 0
        #
        #     # Evaluate metrics on black background
        #     testbed.background_color = [0.0, 0.0, 0.0, 1.0]
        #
        #     # Prior nerf papers don't typically do multi-sample anti aliasing.
        #     # So snap all pixels to the pixel centers.
        #     testbed.snap_to_pixel_centers = True
        #     spp = 8
        #
        #     testbed.nerf.render_min_transmittance = 1e-4
        #
        #     testbed.shall_train = False
        #     testbed.load_training_data(opts.test_transforms)

            # with tqdm(range(testbed.nerf.training.dataset.n_images), unit="images", desc=f"Rendering test frame") as t:
            #     for i in t:
            #         resolution = testbed.nerf.training.dataset.metadata[i].resolution
            #         testbed.render_ground_truth = True
            #         testbed.set_camera_to_training_view(i)
            #         ref_image = testbed.render(resolution[0], resolution[1], 1, True)
            #         testbed.render_ground_truth = False
            #         image = testbed.render(resolution[0], resolution[1], spp, True)
            #
            #         if i == 0:
            #             write_image(f"ref.png", ref_image)
            #             write_image(f"out.png", image)
            #
            #             diffimg = np.absolute(image - ref_image)
            #             diffimg[..., 3:4] = 1.0
            #             write_image("diff.png", diffimg)
            #
            #         A = np.clip(linear_to_srgb(image[..., :3]), 0.0, 1.0)
            #         R = np.clip(linear_to_srgb(ref_image[..., :3]), 0.0, 1.0)
            #         mse = float(compute_error("MSE", A, R))
            #         ssim = float(compute_error("SSIM", A, R))
            #         totssim += ssim
            #         totmse += mse
            #         psnr = mse2psnr(mse)
            #         totpsnr += psnr
            #         minpsnr = psnr if psnr < minpsnr else minpsnr
            #         maxpsnr = psnr if psnr > maxpsnr else maxpsnr
            #         totcount = totcount + 1
            #         t.set_postfix(psnr=totpsnr / (totcount or 1))
            #
            # psnr_avgmse = mse2psnr(totmse / (totcount or 1))
            # psnr = totpsnr / (totcount or 1)
            # ssim = totssim / (totcount or 1)
            # print(f"PSNR={psnr} [min={minpsnr} max={maxpsnr}] SSIM={ssim}")

        if opts.save_mesh is not None:
            res = opts.marching_cubes_res or 256
            thresh = opts.marchines_cubes_thresh or 2.5
            print(
                f"Generating mesh via marching cubes and saving to {opts.save_mesh}. Resolution=[{res},{res},{res}], Density Threshold={thresh}")
            testbed.compute_and_save_marching_cubes_mesh(opts.save_mesh, [res, res, res], thresh=thresh)

