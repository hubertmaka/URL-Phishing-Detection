import ipaddress
import unittest

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
        self.assertRaises(fe.SpaceInUrlException, fe.FeatureExtraction.is_url_proper, 'https:// mysite.pl')

    def testGivenProperUrlWhenCreatingObjectThenReturnTrue(self):
        self.assertTrue(fe.FeatureExtraction.is_url_proper('https://mysite.pl'))

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
        fe1 = fe.FeatureExtraction('https://docs.python.org:443/3/library/urllib.parse.html?highlight=params#url-parsing')
        print(fe1._extract_url_params())

    def testGivenUrlWhenAbnormalNoSchemaNoNetlocUrlThenReturnTrue(self):
        fe1 = fe.FeatureExtraction('garage-pirenne.be/index.php?option=com_')
        print(fe1._extract_url_params())
        self.assertTrue(fe1.abnormal_url)

    def testGivenUrlWhenAbnormalNoNetlocUrlThenReturnTrue(self):
        fe1 = fe.FeatureExtraction('https:/index.php?option=com_')
        print(fe1._extract_url_params())
        self.assertTrue(fe1.abnormal_url)

    def testGivenUrlWhenAbnormalNoSchemaUrlThenReturnTrue(self):
        fe1 = fe.FeatureExtraction('://avc/index.php?option=com_')
        print(fe1._extract_url_params())
        self.assertTrue(fe1.abnormal_url)

    def testGivenUrlWhenNotAbnormalThenReturnTrue(self):
        fe1 = fe.FeatureExtraction('https://docs.python.org:443/3/library/urllib.parse.html?highlight=params#url-parsing')
        print(fe1._extract_url_params())
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


    # def testGivenUrlWhenCheckUrlDepthThenReturnUrlDepth(self):
    #     fe1 = fe.FeatureExtraction('//onet.https.pl')
    #     print(fe1.url_depth)