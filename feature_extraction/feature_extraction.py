import ipaddress
import re

from urllib.parse import urlparse, ParseResult
from feature_extraction.exceptions import SpaceInUrlException
from feature_extraction.utils import PatternCollector


class FeatureExtraction:
    def __init__(self, url: str) -> None:
        if self._is_url_proper(url):
            self.url: str = url.strip()

        self.url_params: ParseResult = urlparse(self.url)
        self._possible_characters = PatternCollector().chars
        self._short_domains = PatternCollector().short_domains
        self._shortening_pattern = self._generate_shortening_regex()

    def _generate_shortening_regex(self):
        return f"https?://(www\.)?({'|'.join(self._short_domains)})"

    @staticmethod
    def _is_url_proper(url: str) -> bool:
        url.strip()
        if ' ' in url:
            raise SpaceInUrlException("URL cannot have space between words", url)

        return True

    @staticmethod
    def _extract_ip_address(url) -> str:
        return url.split('/')[2].lstrip('[').rstrip(']')

    def have_at_sign(self) -> bool:
        return True if '@' in self.url else False

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
        return {ch: self.url.count(ch) for ch in self._possible_characters}

    def have_https(self) -> bool:
        return True if self.url.startswith('https') else False

    @property
    def abnormal_url(self) -> bool:
        netloc, scheme = self.url_params.netloc, self.url_params.scheme
        return True if ((netloc == '') or (scheme == '')) else False

    def count_digits(self) -> int:
        return sum(int(ch.isdigit()) for ch in self.url)

    def count_letters(self) -> int:
        return sum(int(ch.isalpha()) for ch in self.url)

    def path_depth(self) -> int:
        return self.url_params.path.count('/')

    def dots_in_netloc(self) -> int:
        return self.url_params.netloc.count('.')

    def have_shortening_patterns(self) -> bool:
        return bool(re.match(self._shortening_pattern, self.url))

    def have_javascript_code(self) -> bool:
        return True if bool(re.findall(re.compile('<script>'), self.url)) else False



