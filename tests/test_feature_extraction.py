import ipaddress
import unittest
from urllib.parse import urlparse
import feature_extraction as fe


class TestFeatureExtraction(unittest.TestCase):
    def setUp(self) -> None:
        url = 'http://allegr0lokalnie.83473636.xyz/fb7pl5qw'

    def tearDown(self) -> None:
        pass

    def testGivenUrlWhenHaveAtSignThenReturnTrue(self):
        fe1 = fe.FeatureExtraction('https://test@web.com')
        self.assertTrue(fe1.have_at_sign())

    def testGivenUrlWhenNotHaveAtSignThenReturnFalse(self):
        fe1 = fe.FeatureExtraction('https://test.web.com')
        self.assertFalse(fe1.have_at_sign())

    def testGivenUrlWhenHaveIPv4AddressThenReturnTrue(self):
        fe1 = fe.FeatureExtraction('http://192.168.1.1/login.html')
        self.assertTrue(fe1.have_ip_address())

    def testGivenUrlWhenHaveIPv6AddressThenReturnTrue(self):
        fe1 = fe.FeatureExtraction('https://[2001:0db8:85a3:0000:0000:8a2e:0370:7334]/login.html')
        self.assertTrue(fe1.have_ip_address())

    def testGivenUrlWhenNotHaveIPv4AddressThenReturnFalse(self):
        fe1 = fe.FeatureExtraction('https://192.168.1./login.html')
        self.assertFalse(fe1.have_ip_address())

    def testGivenUrlWhenHaveIPv6ShortedAddressThenReturnTrue(self):
        fe1 = fe.FeatureExtraction('https://[2001:db8:85a3::8a2e:37:7334]/login.html')
        self.assertTrue(fe1.have_ip_address())

    def testGivenTwoIPv6AddressesShortedWhenCheckIfEqualThenReturnTrue(self):
        fe1 = '2001:0db8:85a3:0000:0000:8a2e:0370:7334'
        fe2 = '2001:0db8:85a3::8a2e:0370:7334'
        self.assertEqual(ipaddress.ip_address(fe1), ipaddress.ip_address(fe2))

    def testGivenTwoIPv6AddressesShortedAndProperZerosCutWhenCheckIfEqualThenReturnTrue(self):
        url1 = '2001:0db8:85a3:0000:0000:8a2e:0370:7334'
        url2 = '2001:db8:85a3::8a2e:370:7334'
        self.assertEqual(ipaddress.ip_address(url1), ipaddress.ip_address(url2))

    def testGivenTwoIPv6AddressesShortedAndBadZerosCutWhenCheckIfEqualThenReturnFalse(self):
        url1 = '2001:0db8:85a3:0000:0000:8a2e:0370:7334'
        url2 = '2001:db8:85a3::8a2e:37:7334'
        self.assertNotEqual(ipaddress.ip_address(url1), ipaddress.ip_address(url2))

    def testGivenUrlWhenComputeLengthThenReturnProperLength(self):
        fe1 = fe.FeatureExtraction('https://wp.pl')
        self.assertEqual(fe1.url_length, 13)

    def testGivenEmptyStrWhenComputeLengthThenReturnZero(self):
        fe1 = fe.FeatureExtraction('')
        self.assertEqual(fe1.url_length, 0)

    def testGivenUrlWithSpaceBetweenWhenCreatingObjectThenRaiseException(self):
        self.assertRaises(fe.SpaceInUrlException, fe.FeatureExtraction._is_url_proper, 'https:// mysite.pl')

    def testGivenProperUrlWhenCreatingObjectThenReturnTrue(self):
        self.assertTrue(fe.FeatureExtraction._is_url_proper('https://mysite.pl'))

    def testGivenLongerUrlWhenCheckIfUrlLongerThanThresholdThenReturnTrue(self):
        fe1 = fe.FeatureExtraction('https://wp.pl')
        self.assertTrue(fe1.url_longer_than(12))

    def testGivenNotLongerUrlWhenCheckIfUrlLongerThanThresholdThenReturnFalse(self):
        fe1 = fe.FeatureExtraction('https://wp.pl')
        self.assertFalse(fe1.url_longer_than(13))

    def testGivenUrlWithCharsWhenCountCharsThenReturnDictWithCountedChars(self):
        fe1 = fe.FeatureExtraction('htt()p://all@egr$0lo?ka>ln^ie.8347**3636.xyz/fb7pl5qw/;\'\\{}#some-file?%param=abc')
        proper_result = {
            '!': 0, '@': 1, '#': 1,
            '$': 1, '%': 1, '^': 1,
            '&': 0, '*': 2, '(': 1,
            ')': 1, '{': 1, '}': 1,
            '[': 0, ']': 0, '~': 0,
            '`': 0, ':': 1, ';': 1,
            '|': 0, '\\': 1, ',': 0,
            '.': 2, '<': 0, '>': 1,
            '?': 2, '/': 4, '+': 0,
            '=': 1, '-': 1, '_': 0
        }
        self.assertEqual(fe1.count_characters(), proper_result)

    def testGivenEmptyStrWhenCountCharsThenCountAllZeroChars(self):
        fe1 = fe.FeatureExtraction('')
        proper_result = {
            '!': 0, '@': 0, '#': 0,
            '$': 0, '%': 0, '^': 0,
            '&': 0, '*': 0, '(': 0,
            ')': 0, '{': 0, '}': 0,
            '[': 0, ']': 0, '~': 0,
            '`': 0, ':': 0, ';': 0,
            '|': 0, '\\': 0, ',': 0,
            '.': 0, '<': 0, '>': 0,
            '?': 0, '/': 0, '+': 0,
            '=': 0, '-': 0, '_': 0
        }
        self.assertEqual(fe1.count_characters(), proper_result)

    def testGivenUrlStartsWithHTTPSWhenCheckIfStartWithHTTPSThenReturnTrue(self):
        fe1 = fe.FeatureExtraction('https://onet.pl')
        self.assertTrue(fe1.have_https())

    def testGivenUrlNotStartsWithHTTPSWhenCheckIfStartWithHTTPSThenReturnFalse(self):
        fe1 = fe.FeatureExtraction('http://onet.pl')
        self.assertFalse(fe1.have_https())

    def testGivenUrlWithSequenceHTTPSInsideWhenCheckIfStartWithHTTPSThenReturnFalse(self):
        fe1 = fe.FeatureExtraction('//onet.https.pl')
        self.assertFalse(fe1.have_https())

    def testGivenUrlWhenExtractParametersThenReturnProper(self):
        fe1 = fe.FeatureExtraction('https://python.org:443/3/library/urllib.html?highlight=params#url')
        self.assertEqual(fe1.url_params, urlparse('https://python.org:443/3/library/urllib.html?highlight=params#url'))

    def testGivenUrlWhenAbnormalNoSchemaNoNetlocUrlThenReturnTrue(self):
        fe1 = fe.FeatureExtraction('garage-pirenne.be/index.php?option=com_')
        self.assertTrue(fe1.abnormal_url)

    def testGivenUrlWhenAbnormalNoNetlocUrlThenReturnTrue(self):
        fe1 = fe.FeatureExtraction('https:/index.php?option=com_')
        self.assertTrue(fe1.abnormal_url)

    def testGivenUrlWhenAbnormalNoSchemaUrlThenReturnTrue(self):
        fe1 = fe.FeatureExtraction('://avc/index.php?option=com_')
        self.assertTrue(fe1.abnormal_url)

    def testGivenUrlWhenNotAbnormalThenReturnTrue(self):
        fe1 = fe.FeatureExtraction('https://docs.python.org:443/3/library/urllib.parse.html?highlight=params#url-parsing')
        self.assertFalse(fe1.abnormal_url)

    def testGivenUrlWhenCountZeroDigitsInUrlThenReturnZero(self):
        fe1 = fe.FeatureExtraction('https://docs.python.org/library/urllib.parse.html?highlight=params#url-parsing')
        self.assertEqual(fe1.count_digits(), 0)

    def testGivenUrlWhenCountSomeDigitsInUrlThenReturnZero(self):
        fe1 = fe.FeatureExtraction('https://docs.pyth57on.org:653/library/ur124llib.parse089.html?hit=params#url-1par')
        self.assertEqual(fe1.count_digits(), 12)

    def testGivenUrlWhenCountZeroAlphaThenReturnZero(self):
        fe1 = fe.FeatureExtraction('65345::////13123')
        self.assertEqual(fe1.count_letters(), 0)

    def testGivenUrlWhenCountSomeAlphaThenReturnZero(self):
        fe1 = fe.FeatureExtraction('https://wp.pl/65345::////13123')
        self.assertEqual(fe1.count_letters(), 9)

    def testGivenPathWhenCountDepthNonZeroThenReturnNumberOfSlashes(self):
        fe1 = fe.FeatureExtraction('https://wp.pl/65345/abcd/ab;cd/?param1=ddd')
        self.assertEqual(fe1.path_depth(), 4)

    def testGivenPathWhenCountDepthZeroThenReturnZero(self):
        fe1 = fe.FeatureExtraction('https://wp.pl?param=ddd')
        self.assertEqual(fe1.path_depth(), 0)

    def testGivenNetlocWhenCountDotsNonZeroThenReturnNumberOfDots(self):
        fe1 = fe.FeatureExtraction('https://www.google.com/abc.com')
        self.assertEqual(fe1.dots_in_netloc(), 2)

    def testGivenNetlocWhenCountDotsZeroDotsThenReturnZEro(self):
        fe1 = fe.FeatureExtraction('https:///abc.com')
        self.assertEqual(fe1.dots_in_netloc(), 0)

    def testGivenShortDomainsWhenGenerateShortDomainsPatternThenReturnPattern(self):
        fe1 = fe.FeatureExtraction('')
        self.assertEqual(fe1._generate_shortening_regex(), 'https?://(www\.)?(bit.ly|goo.gl|tinyurl.com|t.co|ow.ly|is.gd|shorte.st|adf.ly|bc.vc|cli.gs|cutt.us|u.to|j.mp|v.gd|qr.ae|tr.im|prettylinkpro.com|yourls.org|slink.be|scrnch.me|filoops.info|vzturl.com|x.co|zzb.bz|1url.com|tweez.me|v.tl|lnkd.in|dft.ba|yep.it|hurl.me|url.ie|link.zip.net|cort.as|po.st|4sq.com|1u.bb|awk.fr|buzurl.com|cutt.ly|t2m.io|waa.ai|get.shorty|tiny.cc|short.to|snip.ly|pt.link|cl.lk|soo.gd|ity.im|yfrog.com|twitthis.com|u.nu|plurl.me|urlx.ie|poprl.com|to.ly|bit.do|rb.gy|shorturl.at|clicky.me|budurl.com|trim.li|qr.net|url.kz|ur2.me|2.tu|zpag.es|xlink.me|goshrink.com|picz.us|tinyarrows.net|chilp.it|nanoref.com|notlong.com|post.ly|xrl.us|url4.eu|virl.ws|migre.me|buk.me|cuturls.com|fun.ly|snipurl.com|golinks.co|viralurl.biz|twurl.nl|merky.de)')

    def testGivenBitlyUrlWhenMatchesPatternThenReturnTrue(self):
        fe1 = fe.FeatureExtraction('https://bit.ly/3uQFzJq')
        self.assertTrue(fe1.have_shortening_patterns())

    def testGivenTinyUrlWhenMatchesPatternThenReturnTrue(self):
        fe1 = fe.FeatureExtraction('https://tinyurl.com/yz3u9j2a')
        self.assertTrue(fe1.have_shortening_patterns())

    def testGivenGoogleUrlWhenMatchesPatternThenReturnTrue(self):
        fe1 = fe.FeatureExtraction('https://goo.gl/maps/abc123')
        self.assertTrue(fe1.have_shortening_patterns())

    def testGivenTwitterUrlWhenMatchesPatternThenReturnTrue(self):
        fe1 = fe.FeatureExtraction('https://t.co/ABCD1234')
        self.assertTrue(fe1.have_shortening_patterns())

    def testGivenOwlyUrlWhenMatchesPatternThenReturnTrue(self):
        fe1 = fe.FeatureExtraction('https://ow.ly/xYzA1')
        self.assertTrue(fe1.have_shortening_patterns())

    def testGivenTinyCCUrlWhenMatchesPatternThenReturnTrue(self):
        fe1 = fe.FeatureExtraction('https://tiny.cc/abc123')
        self.assertTrue(fe1.have_shortening_patterns())

    def testGivenUrlWithScriptWhenCheckIfJavaScriptInUrlThenReturnTrue(self):
        fe1 = fe.FeatureExtraction('https://code.jquery.com/jquery-3<script>alert("Hello")</script>')
        self.assertTrue(fe1.have_javascript_code())

    def testGivenUrlWithoutScriptWhenCheckIfJavaScriptInUrlThenReturnFalse(self):
        fe1 = fe.FeatureExtraction('https://code.jquery.com/jquery-3alert("Hello")')
        self.assertFalse(fe1.have_javascript_code())
