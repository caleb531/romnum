#!/usr/bin/env python3

import json
import unittest

from romnum import encode, decode, RomanNumeralException


def get_encoding_test_cases():
    with open('encoding_test_cases.json', 'r') as encoding_map_file:
        return json.load(encoding_map_file)


def get_decoding_test_cases():
    return {value: key for key, value in get_encoding_test_cases().items()}


class TestEncode(unittest.TestCase):

    def test_encode(self):
        for integer, romnum in get_encoding_test_cases().items():
            with self.subTest(integer=int(integer)):
                self.assertEqual(encode(int(integer)), romnum)


class TestDecode(unittest.TestCase):

    def test_decode(self):
        for romnum, integer in get_decoding_test_cases().items():
            with self.subTest(romnum=romnum):
                self.assertEqual(decode(romnum), int(integer))

    def test_invalid_order(self):
        with self.assertRaises(RomanNumeralException):
            decode('CMMVII')

    def test_invalid_repetition(self):
        with self.assertRaises(RomanNumeralException):
            decode('CXXXXII')


if __name__ == '__main__':
    unittest.main()
