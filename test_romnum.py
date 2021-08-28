#!/usr/bin/env python3

import json
import nose.tools as nose

from romnum import encode, decode, RomanNumeralException


def get_encoding_test_cases():
    with open('encoding_test_cases.json', 'r') as encoding_map_file:
        return json.load(encoding_map_file)


def get_decoding_test_cases():
    return {value: key for key, value in get_encoding_test_cases().items()}


class TestEncode(object):

    def test_encode(self):
        for integer, romnum in get_encoding_test_cases().items():
            yield nose.assert_equal, encode(int(integer)), romnum

    def test_invalid_integer(self):
        with nose.assert_raises(TypeError):
            encode('abc')


class TestDecode(object):

    def test_decode(self):
        for romnum, integer in get_decoding_test_cases().items():
            yield nose.assert_equal, decode(romnum), int(integer)

    def test_invalid_order(self):
        with nose.assert_raises(RomanNumeralException):
            decode('CMMVII')

    def test_invalid_repetition(self):
        with nose.assert_raises(RomanNumeralException):
            decode('CXXXXII')

    def test_invalid_case(self):
        with nose.assert_raises(RomanNumeralException):
            decode('mmxviii')

    def test_invalid_characters(self):
        with nose.assert_raises(RomanNumeralException):
            decode('xyz')
