#!/usr/bin/env python3

import json
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

import pytest

from romnum import RomanNumeralException, decode, encode, main


def get_encoding_test_cases():
    encoding_path = Path("tests") / "encoding_test_cases.json"
    with encoding_path.open("r", encoding="utf-8") as encoding_map_file:
        raw_cases = json.load(encoding_map_file)
    return {int(integer): romnum for integer, romnum in raw_cases.items()}


def get_decoding_test_cases():
    return {romnum: integer for integer, romnum in get_encoding_test_cases().items()}


@pytest.mark.parametrize(("integer", "romnum"), get_encoding_test_cases().items())
def test_encode(integer, romnum):
    assert encode(integer) == romnum


def test_invalid_integer():
    with pytest.raises(RomanNumeralException):
        encode("abc")


@patch("sys.argv", ["romnum.pyr", "encode", "47"])
def test_main_encode():
    with redirect_stdout(StringIO()) as out:
        main()
        assert out.getvalue().rstrip() == "XLVII"


@pytest.mark.parametrize(("romnum", "integer"), get_decoding_test_cases().items())
def test_decode(romnum, integer):
    assert decode(romnum) == integer


def test_invalid_order():
    with pytest.raises(RomanNumeralException):
        decode("CMMVII")


def test_invalid_repetition():
    with pytest.raises(RomanNumeralException):
        decode("CXXXXII")


def test_invalid_case():
    with pytest.raises(RomanNumeralException):
        decode("mmxviii")


def test_invalid_characters():
    with pytest.raises(RomanNumeralException):
        decode("xyz")


@patch("sys.argv", ["romnum.pyr", "decode", "XLVII"])
def test_main_decode():
    with redirect_stdout(StringIO()) as out:
        main()
        assert out.getvalue().rstrip() == "47"
