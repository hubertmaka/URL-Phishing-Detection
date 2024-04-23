class SpaceInUrlException(Exception):
    def __init__(self, errText: str, invalidUrl: str):
        super().__init__(errText, invalidUrl)

