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
        self.assertTrue(fe1.haveAtSign())

    def testGivenUrlWhenNotHaveAtSignThenReturnFalse(self):
        fe1 = fe.FeatureExtraction('https://test.web.com')
        self.assertFalse(fe1.haveAtSign())

    def testGivenUrlWhenHaveIPv4AddressThenReturnTrue(self):
        fe1 = fe.FeatureExtraction('http://192.168.1.1/login.html')
        self.assertTrue(fe1.haveIPAddress())

    def testGivenUrlWhenHaveIPv6AddressThenReturnTrue(self):
        fe1 = fe.FeatureExtraction('https://[2001:0db8:85a3:0000:0000:8a2e:0370:7334]/login.html')
        self.assertTrue(fe1.haveIPAddress())

    def testGivenUrlWhenNotHaveIPv4AddressThenReturnFalse(self):
        fe1 = fe.FeatureExtraction('https://192.168.1./login.html')
        self.assertFalse(fe1.haveIPAddress())

    def testGivenUrlWhenHaveIPv6ShortedAddressThenReturnTrue(self):
        fe1 = fe.FeatureExtraction('https://[2001:db8:85a3::8a2e:37:7334]/login.html')
        self.assertTrue(fe1.haveIPAddress())

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
        self.assertEqual(fe1.urlLength, 13)

    def testGivenEmptyStrWhenComputeLengthThenReturnZero(self):
        fe1 = fe.FeatureExtraction('')
        self.assertEqual(fe1.urlLength, 0)

    def testGivenUrlWithSpaceBetweenWhenCreatingObjectThenRaiseException(self):
        self.assertRaises(fe.SpaceInUrlException, fe.FeatureExtraction.isUrlProper, 'https:// mysite.pl')

    def testGivenProperUrlWhenCreatingObjectThenReturnTrue(self):
        self.assertTrue(fe.FeatureExtraction.isUrlProper('https://mysite.pl'))

    def testGivenLongerUrlWhenCheckIfUrlLongerThanThresholdThenReturnTrue(self):
        fe1 = fe.FeatureExtraction('https://wp.pl')
        self.assertTrue(fe1.urlLongerThan(12))

    def testGivenNotLongerUrlWhenCheckIfUrlLongerThanThresholdThenReturnFalse(self):
        fe1 = fe.FeatureExtraction('https://wp.pl')
        self.assertFalse(fe1.urlLongerThan(13))
