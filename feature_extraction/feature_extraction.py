import ipaddress
import re
from urllib.parse import urlparse, ParseResult
from feature_extraction.exceptions import SpaceInUrlException


class FeatureExtraction:
    def __init__(self, url: str) -> None:
        if self.is_url_proper(url):
            self.url = url.strip()

        self.possible_characters = [
            '!', '@', '#', '$', '%',
            '^', '&', '*', '(', ')',
            '{', '}', '[', ']', '~',
            '`', ':', ';', '|', '\\',
            ',', '.', '<', '>', '?',
            '/', '+', '=', '-', '_'
        ]

    def have_at_sign(self) -> bool:
        return True if '@' in self.url else False

    @staticmethod
    def is_url_proper(url: str) -> bool:
        url.strip()
        if ' ' in url:
            raise SpaceInUrlException("URL cannot have space between words", url)

        return True

    @staticmethod
    def _extract_ip_address(url) -> str:
        return url.split('/')[2].lstrip('[').rstrip(']')

    def have_ip_address(self) -> bool:
        try:
            ipaddress.ip_address(self._extract_ip_address(self.url))
            return True
        except ValueError:
            return False

    @property
    def url_length(self) -> int:
        return len(self.url)

    def url_longer_than(self, comp_len: int) -> bool:
        return True if len(self.url) > comp_len else False

    def count_characters(self) -> dict[str: int]:
        return {ch: self.url.count(ch) for ch in self.possible_characters}

    def have_https(self) -> bool:
        return True if self.url.startswith('https') else False

    def _extract_url_params(self) -> ParseResult:
        return urlparse(self.url)

    # @property
    # def url_depth(self):
    #     return sum(self.url.split('/')[2:])

    @property
    def abnormal_url(self) -> bool:
        netloc, scheme = str(urlparse(self.url).netloc), str(urlparse(self.url).scheme)
        return True if ((netloc == '') or (scheme == '')) else False

    def count_digits(self):
        return sum(int(ch.isdigit()) for ch in self.url)

    def count_letters(self):
        return sum(int(ch.isalpha()) for ch in self.url)

    # TODO: shortening patterns, javascript in url, number of dots in domain,
