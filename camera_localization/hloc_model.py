from pathlib import Path
from hloc import extract_features, match_features, reconstruction, pairs_from_exhaustive
from .common import colmap2TransformsJson, run_colmap_model_converter


class HLOCPredictOptions:
    def __init__(self, path, images_folder, output_path, aabb_scale=32, skip_early=0, text='colmap_text'):
        """
        :param path: Path that contains images_folder
        :param images_folder: name of images_folder
        :param output_path: output_path of hloc
        """
        self.path = path
        self.output_path = output_path
        self.images_folder = images_folder
        self.aabb_scale = aabb_scale
        self.skip_early = skip_early
        self.text = text


class HLOCModel:
    def __init__(self):
        super().__init__()

    def predict(self, opts: HLOCPredictOptions):
        # Define the paths
        images = Path(opts.path) / opts.images_folder
        outputs = Path(opts.path)

        sfm_pairs = outputs / 'pairs-sfm.txt'
        loc_pairs = outputs / 'pairs-loc.txt'
        sfm_dir = outputs / opts.text
        features = outputs / 'features.h5'
        matches = outputs / 'matches.h5'

        # Configuration for features and matcher
        feature_conf = extract_features.confs['disk']
        matcher_conf = match_features.confs['disk+lightglue']

        # List of reference images
        references = [str(p.relative_to(images)) for p in images.iterdir()]
        print(len(references), "mapping images")

        # Run the feature extraction, pairs generation, and feature matching
        extract_features.main(feature_conf, images, image_list=references, feature_path=features)
        pairs_from_exhaustive.main(sfm_pairs, image_list=references)
        match_features.main(matcher_conf, sfm_pairs, features=features, matches=matches)
        reconstruction.main(sfm_dir, images, sfm_pairs, features, matches, image_list=references)
        run_colmap_model_converter(input_path=sfm_dir, output_path=sfm_dir, output_type='TXT')
        colmap2TransformsJson(aabb_scale=opts.aabb_scale,
                              skip_early=opts.skip_early,
                              path=opts.path,
                              output_path=opts.output_path,
                              images_folder=opts.images_folder,
                              text=opts.text)
