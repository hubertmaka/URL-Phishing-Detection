import ipaddress
import re
from urllib.parse import urlparse, ParseResult
from feature_extraction.utils import PatternCollector


class FeatureExtraction:
    """Extracts features from URLs."""

    def __init__(self, url: str) -> None:
        """Initialize the FeatureExtraction instance.

        Args:
            url (str): The URL to extract features from.
        """

        self.url: str = url.strip().replace(' ', '+')
        self.url = self._reduce_empty_path()
        self.url_params: ParseResult = self._load_params()
        self._possible_characters = PatternCollector().chars
        self._short_domains = PatternCollector().short_domains
        self._shortening_pattern = self._generate_shortening_regex()

    def _load_params(self) -> ParseResult:
        """Load parameters from the urlparse and given URL.

        Returns:
            ParseResult: The parsed parts of URL
        """
        try:
            if re.match("https?://", self.url):
                return urlparse(self.url)
            else:
                return urlparse("noscheme://" + self.url)
        except ValueError:
            return urlparse(self.url.replace('[', '').replace(']', ''))


    def _reduce_empty_path(self):
        """Reduce the / from url when the path contains only /.

        Returns:
            str: The reduced url or the original.
        """
        return self.url[:-1] if (self._load_params().path == '/' and self.url.endswith('/')) else self.url

    def _generate_shortening_regex(self) -> str:
        """Generate a regular expression pattern for shortening services."""
        return f"https?://(www\.)?({'|'.join(self._short_domains)})"

    def _extract_ip_address(self, url) -> str:
        """Extract the IP address from the URL."""
        return str(self.url_params.netloc).lstrip('[').rstrip(']')

    def have_at_sign(self) -> bool:
        """Check if the URL contains the '@' symbol.

        Returns:
            bool: True if the URL contains '@', False otherwise.
        """
        return True if '@' in self.url else False

    def have_ip_address(self) -> bool:
        """Check if the URL contains an IP address.

        Returns:
            bool: True if the URL contains an IP address, False otherwise.
        """
        try:
            ipaddress.ip_address(self._extract_ip_address(self.url))
            return True
        except ValueError:
            return False

    @property
    def url_length(self) -> int:
        """Get the length of the URL.

        Returns:
            int: The length of the URL.
        """
        return len(self.url)

    def url_longer_than(self, comp_len: int) -> bool:
        """Check if the URL is longer than a given length.

        Args:
            comp_len (int): The length to compare.

        Returns:
            bool: True if the URL is longer than the given length, False otherwise.
        """
        return True if len(self.url) > comp_len else False

    def count_characters(self) -> dict:
        """Count the occurrences of special characters in the URL.

        Returns:
            dict: A dictionary where keys are special characters and values are their counts.
        """
        return {ch: self.url.count(ch) for ch in self._possible_characters}

    def have_https(self) -> bool:
        """Check if the URL starts with 'https'.

        Returns:
            bool: True if the URL starts with 'https', False otherwise.
        """
        return True if self.url.startswith('https') else False

    @property
    def abnormal_url(self) -> bool:
        """Check if the URL is abnormal (missing scheme or netloc or have 0 letters in url).

        Returns:
            bool: True if the URL is abnormal, False otherwise.
        """
        netloc, scheme = self.url_params.netloc, self.url_params.scheme
        return True if ((netloc == '') or
                        (scheme == 'noscheme') or
                        (self.count_letters() == 0) or
                        (self.dots_in_netloc() < 1)) else False

    def count_digits(self) -> int:
        """Count the number of digits in the URL.

        Returns:
            int: The number of digits in the URL.
        """
        return sum(int(ch.isdigit()) for ch in self.url)

    def count_letters(self) -> int:
        """Count the number of letters in the URL.

        Returns:
            int: The number of letters in the URL.
        """
        return sum(int(ch.isalpha()) for ch in self.url)

    def path_depth(self) -> int:
        """Count the depth of the path in the URL.

        Returns:
            int: The depth of the path in the URL.
        """
        return self.url_params.path.count('/')

    def dots_in_netloc(self) -> int:
        """Count the number of dots in the netloc part of the URL.

        Returns:
            int: The number of dots in the netloc part of the URL.
        """
        return self.url_params.netloc.count('.')

    def netloc_length(self) -> int:
        """Count the netloc (domain) length.

        Returns:
            int: Netloc length.
        """
        return len(self.url_params.netloc)

    def have_shortening_patterns(self) -> bool:
        """Check if the URL matches any shortening service patterns.

        Returns:
            bool: True if the URL matches shortening service patterns, False otherwise.
        """
        return bool(re.match(self._shortening_pattern, self.url))

    def have_javascript_code(self) -> bool:
        """Check if the URL contains JavaScript code.

        Returns:
            bool: True if the URL contains JavaScript code, False otherwise.
        """
        return True if bool(re.findall(re.compile('<script>'), self.url)) else False

    def have_www_in_netloc(self) -> bool:
        """Check if in the netloc is www prefix.

        Returns:
            bool: True if the Netloc contains www prefix, False otherwise.
        """
        return True if self.url_params.netloc.startswith('www.') else False

    def in_top_100(self) -> bool:
        """Check if the netloc is in top 100 popular domains.

        Returns:
            bool: True if the netloc is in top 100 popular domains, False otherwise.
        """
        return True if (self.url_params.netloc in PatternCollector.top_100_urls) else False

    def count_slashes_in_path(self) -> int:
        """Count the number of slashes in path in the URL.

        Returns:
             int: Number of slashes in path.
        """
        return self.url_params.path.count('/')

    def count_words_in_netloc(self) -> int:
        """Count the number of words in netloc.

        Return: Number of words in netloc.
        """
        return len(self.url_params.netloc.split('.'))
    # TODO: Dorobić funkcję która policzy ilość / w ścieżce. oraz ilość słów w domenie. Oraz może dodać kilka modeli i zobaczyć który co wykryje jak najlepiej.