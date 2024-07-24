from glob import glob
import shutil
from enum import Enum
from pathlib import Path
from .common import *

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
SCRIPTS_FOLDER = os.path.join(ROOT_DIR, "scripts")


class ColmapMatchers(Enum):
    sequential = 0
    exhaustive = 1
    spatial = 2
    transitive = 3
    vocab_tree = 4


class ColmapCameraModel(Enum):
    SIMPLE_PINHOLE = 0
    PINHOLE = 1
    SIMPLE_RADIAL = 2
    RADIAL = 3
    OPENCV = 4
    SIMPLE_RADIAL_FISHEYE = 5
    RADIAL_FISHEYE = 6
    OPENCV_FISHEYE = 7


class ColmapLocalizationPredictOptions:
    def __init__(self, path, images_folder, output_path='transforms.json', video_in=None, video_fps=2, time_slice="",
                 run_colmap=True, colmap_matcher: ColmapMatchers = ColmapMatchers.exhaustive, colmap_db="colmap.db",
                 colmap_camera_model: ColmapCameraModel = ColmapCameraModel.OPENCV, colmap_camera_params="",
                 text="colmap_text", aabb_scale=32, skip_early=0, keep_colmap_coords=True,
                 vocab_path="", mask_categories=[]):
        """
        :param video_in: Run ffmpeg first to convert a provided video file into a set of images. Uses the video_fps parameter also.
        :param video_fps: Fps of input video
        :param time_slice: Time (in seconds) in the format t1,t2 within which the images should be generated from the video. E.g.: \"--time_slice '10,300'\" will generate images only from 10th second to 300th second of the video.
        :param run_colmap: run colmap first on the image folder
        :param colmap_matcher: Select which matcher colmap should use. Sequential for videos, exhaustive for ad-hoc images.
        :param colmap_db: colmap database filename
        :param colmap_camera_model: Camera model
        :param colmap_camera_params: Intrinsic parameters, depending on the chosen model. Format: fx,fy,cx,cy,dist
        :param path: Input path to the images.
        :param text: Input path to the colmap text files (set automatically if --run_colmap is used).
        :param aabb_scale: Large scene scale factor. 1=scene fits in unit cube; power of 2 up to 128
        :param skip_early: Skip this many images from the start.
        :param keep_colmap_coords: Keep transforms.json in COLMAP's original frame of reference (this will avoid reorienting and repositioning the scene for preview and rendering).
        :param vocab_path: Vocabulary tree path.
        :param mask_categories: Object categories that should be masked out from the training images. See `scripts/category2id.json` for supported categories.
        """

        self.video_in = video_in
        self.video_fps = video_fps
        self.time_slice = time_slice
        self.run_colmap = run_colmap
        self.colmap_matcher = colmap_matcher
        self.colmap_db = colmap_db
        self.colmap_camera_model = colmap_camera_model
        self.colmap_camera_params = colmap_camera_params
        self.path = path
        self.images_folder = images_folder
        self.text = text
        self.aabb_scale = aabb_scale
        self.skip_early = skip_early
        self.keep_colmap_coords = keep_colmap_coords
        self.output_path = output_path
        self.vocab_path = vocab_path
        self.overwrite = True
        self.mask_categories = mask_categories


class ColMapLocalization:

    def run_ffmpeg(self, args: ColmapLocalizationPredictOptions):
        ffmpeg_binary = "ffmpeg"

        # On Windows, if FFmpeg isn't found, try automatically downloading it from the internet
        if os.name == "nt" and os.system(f"where {ffmpeg_binary} >nul 2>nul") != 0:
            ffmpeg_glob = os.path.join(ROOT_DIR, "external", "ffmpeg", "*", "bin", "ffmpeg.exe")
            candidates = glob(ffmpeg_glob)
            if not candidates:
                print("FFmpeg not found. Attempting to download FFmpeg from the internet.")
                do_system(os.path.join(SCRIPTS_FOLDER, "download_ffmpeg.bat"))
                candidates = glob(ffmpeg_glob)

            if candidates:
                ffmpeg_binary = candidates[0]

        if not os.path.isabs(args.images):
            args.images = os.path.join(os.path.dirname(args.video_in), args.images)

        images = "\"" + args.images + "\""
        video = "\"" + args.video_in + "\""
        fps = float(args.video_fps) or 1.0
        print(f"running ffmpeg with input video file={video}, output image folder={images}, fps={fps}.")
        if not args.overwrite and (
                                          input(
                                              f"warning! folder '{images}' will be deleted/replaced. continue? (Y/n)").lower().strip() + "y")[
                                  :1] != "y":
            sys.exit(1)
        try:
            # Passing Images' Path Without Double Quotes
            shutil.rmtree(args.images)
        except:
            pass
        do_system(f"mkdir {images}")

        time_slice_value = ""
        time_slice = args.time_slice
        if time_slice:
            start, end = time_slice.split(",")
            time_slice_value = f",select='between(t\,{start}\,{end})'"
        do_system(
            f"{ffmpeg_binary} -i {video} -qscale:v 1 -qmin 1 -vf \"fps={fps}{time_slice_value}\" {images}/%04d.jpg")

    def run_colmap(self, args):
        colmap_binary = find_colmap()

        db = os.path.abspath(os.path.join(args.path, args.colmap_db))
        images = "\"" + os.path.abspath(os.path.join(args.path, args.images_folder)) + "\""
        db_noext = os.path.abspath(os.path.join(args.path, str(Path(db).with_suffix(""))))

        if args.text == "text":
            args.text = db_noext + "_text"
        text = os.path.abspath(os.path.join(args.path, args.text))
        sparse = db_noext + "_sparse"
        print(f"running colmap with:\n\tdb={db}\n\timages={images}\n\tsparse={sparse}\n\ttext={text}")
        if not args.overwrite and (
                                          input(
                                              f"warning! folders '{sparse}' and '{text}' will be deleted/replaced. continue? (Y/n)").lower().strip() + "y")[
                                  :1] != "y":
            sys.exit(1)
        if os.path.exists(db):
            os.remove(db)
        do_system(
            f"{colmap_binary} feature_extractor --ImageReader.camera_model {args.colmap_camera_model.name} --ImageReader.camera_params \"{args.colmap_camera_params}\" --SiftExtraction.estimate_affine_shape=true --SiftExtraction.domain_size_pooling=true --ImageReader.single_camera 1 --database_path {db} --image_path {images}")
        match_cmd = f"{colmap_binary} {args.colmap_matcher.name}_matcher --SiftMatching.guided_matching=true --database_path {db}"
        if args.vocab_path:
            match_cmd += f" --VocabTreeMatching.vocab_tree_path {args.vocab_path}"
        do_system(match_cmd)
        try:
            shutil.rmtree(sparse)
        except:
            pass
        do_system(f"mkdir {sparse}")
        do_system(f"{colmap_binary} mapper --database_path {db} --image_path {images} --output_path {sparse}")
        do_system(
            f"{colmap_binary} bundle_adjuster --input_path {sparse}/0 --output_path {sparse}/0 --BundleAdjustment.refine_principal_point 1")
        try:
            shutil.rmtree(text)
        except:
            pass
        do_system(f"mkdir {text}")
        do_system(
            f"{colmap_binary} model_converter --input_path {sparse}/0 --output_path {text} --output_type TXT")

    def predict(self, args: ColmapLocalizationPredictOptions):
        if args.video_in is not None:
            self.run_ffmpeg(args)
        if args.run_colmap:
            self.run_colmap(args)
        colmap2TransformsJson(aabb_scale=args.aabb_scale,
                              skip_early=args.skip_early,
                              path=args.path,
                              images_folder=args.images_folder,
                              text=args.text,
                              output_path=args.output_path)
