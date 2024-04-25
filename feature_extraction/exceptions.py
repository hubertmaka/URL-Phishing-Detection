class SpaceInUrlException(Exception):
    def __init__(self, err_text: str, invalid_url: str):
        super().__init__(f'{err_text}: {invalid_url}')

