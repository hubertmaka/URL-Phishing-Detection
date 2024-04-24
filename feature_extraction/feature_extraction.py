import ipaddress
from feature_extraction.exceptions import SpaceInUrlException


class FeatureExtraction:
    def __init__(self, url: str) -> None:
        if self.isUrlProper(url):
            self.url = url.strip()

        self.possibleCharacters = [
            '!', '@', '#', '$', '%',
            '^', '&', '*', '(', ')',
            '{', '}', '[', ']', '~',
            '`', ':', ';', '|', '\\',
            ',', '.', '<', '>', '?',
            '/', '+', '=', '-', '_'
        ]

    def haveAtSign(self) -> bool:
        return True if '@' in self.url else False

    @staticmethod
    def isUrlProper(url: str) -> bool:
        url.strip()
        if ' ' in url:
            raise SpaceInUrlException("URL cannot have space between words", url)

        return True

    @staticmethod
    def _extractIPvAddress(url) -> str:
        return url.split('/')[2].lstrip('[').rstrip(']')

    def haveIPAddress(self) -> bool:
        try:
            ipaddress.ip_address(self._extractIPvAddress(self.url))
            return True
        except ValueError:
            return False

    @property
    def urlLength(self) -> int:
        return len(self.url)

    def urlLongerThan(self, comp_len: int) -> bool:
        return True if len(self.url) > comp_len else False

    @property
    def urlDepth(self):
        return sum(self.url.split('/')[2:])

    def countCharacters(self):
        charCounts: dict[str: int] = {}
        for ch in self.possibleCharacters:
            charCounts[ch] = self.url.count(ch)
        return charCounts

    def haveHttps(self):
        return True if self.url.startswith('https') else False


