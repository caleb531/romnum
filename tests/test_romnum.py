#!/usr/bin/env python3

import json
import unittest
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

from romnum import RomanNumeralException, decode, encode, main


def get_encoding_test_cases():
    with open("tests/encoding_test_cases.json", "r") as encoding_map_file:
        return json.load(encoding_map_file)


def get_decoding_test_cases():
    return {value: key for key, value in get_encoding_test_cases().items()}


class TestEncode(unittest.TestCase):

    def test_encode(self):
        for integer, romnum in get_encoding_test_cases().items():
            yield self.assertEqual, encode(int(integer)), romnum

    def test_invalid_integer(self):
        with self.assertRaises(RomanNumeralException):
            encode("abc")

    @patch("sys.argv", ["romnum.pyr", "encode", "47"])
    def test_main(self):
        with redirect_stdout(StringIO()) as out:
            main()
            self.assertEqual(out.getvalue().rstrip(), "XLVII")


class TestDecode(unittest.TestCase):

    def test_decode(self):
        for romnum, integer in get_decoding_test_cases().items():
            yield self.assertEqual, decode(romnum), int(integer)

    def test_invalid_order(self):
        with self.assertRaises(RomanNumeralException):
            decode("CMMVII")

    def test_invalid_repetition(self):
        with self.assertRaises(RomanNumeralException):
            decode("CXXXXII")

    def test_invalid_case(self):
        with self.assertRaises(RomanNumeralException):
            decode("mmxviii")

    def test_invalid_characters(self):
        with self.assertRaises(RomanNumeralException):
            decode("xyz")

    @patch("sys.argv", ["romnum.pyr", "decode", "XLVII"])
    def test_main(self):
        with redirect_stdout(StringIO()) as out:
            main()
            self.assertEqual(out.getvalue().rstrip(), "47")
