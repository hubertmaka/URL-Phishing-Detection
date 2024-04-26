class SpaceInUrlException(Exception):
    """Exception raised for URLs containing spaces.

    Attributes:
        err_text (str): The error message text.
        invalid_url (str): The invalid URL causing the exception.
    """

    def __init__(self, err_text: str, invalid_url: str):
        """Initialize the SpaceInUrlException.

        Args:
            err_text (str): The error message text.
            invalid_url (str): The invalid URL causing the exception.
        """
        super().__init__(f'{err_text}: {invalid_url}')

