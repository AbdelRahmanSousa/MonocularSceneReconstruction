class PPWizard:
    def __init__(self):
        pass

    def preprocess(self, data):
        """
        :param data: an array of images
        :return: an array of preprocessed images
        """
        pass

    @staticmethod
    def run_pipeline(item, wizard_pipeline):
        """
        :param wizard_pipeline: A list of PPWizards that are run in ascending order according to index, where the output
        of the first item is given to the second item, etc...
        :param item: the item that is given to the first element in the pipeline
        :return: The item after being modified by the pipeline
        """

        curr_item = [item]
        for wizard in wizard_pipeline:
            curr_item = wizard.preprocess(curr_item)
        return curr_item
