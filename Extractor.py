# Base class for keyword extractors


class Extractor:
    """Extractor parses a block of text and extracts keywords relevant to the
    article"""

    def __init__(self):
        pass

    def analyze(self, article):
        pass

    def get_keywords(self, article):
        pass

    def rank_keywords(self, article):
        pass


