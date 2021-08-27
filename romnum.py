#!/usr/bin/env python3

import argparse
import json
import re


# A regular expression for describing strict Roman Numeral syntax
ROMNUM_PATT = (r'^(?=[MDCLXVI])M*'
               r'(C[MD]|D?C{0,3})'
               r'(X[CL]|L?X{0,3})'
               r'(I[XV]|V?I{0,3})$')


# A dedicated Roman Numeral exception class which does not have any special
# behavior; it purely exists for semantic purposes
class RomanNumeralException(Exception):
    pass


# Return a dictionary map used for encoding common integers to their roman
# numeral equivalents
def get_encoding_map():
    with open('encoding_map.json', 'r') as encoding_map_file:
        return json.load(encoding_map_file)


# Return a dictionary map used for decoding common roman numerals to their
# integer equivalents
def get_decoding_map():
    return {value: key for key, value in get_encoding_map().items()}


# Encode the given integer as a roman numeral
def encode(integer):

    encoding_map = get_encoding_map()
    romnum_parts = []
    for i in reversed(range(len(str(integer)))):
        integer_part = (integer % (10**(i + 1))) - (integer % (10**i))
        if str(integer_part) in encoding_map:
            romnum_parts.append(encoding_map[str(integer_part)])
        elif integer_part % 1000 == 0:
            romnum_parts.append(encoding_map['1000'] * (integer_part // 1000))

    return ''.join(romnum_parts)


def decode(romnum):

    # Verify immediately if the given Roman Numeral is syntactically correct
    # before performing any conversion
    if not re.search(ROMNUM_PATT, romnum):
        raise RomanNumeralException('Invalid Roman Numeral: {}'.format(
            romnum))

    decoding_map = get_decoding_map()
    partial_romnum = ''
    running_total = 0
    for romnum_letter in romnum:
        # Find each longest base roman numeral within the given roman numeral
        # and convert it to an integer; the sum of all these partial sums is
        # the final decoded integer (e.g. MXCVIII)
        if ((partial_romnum + romnum_letter) not in decoding_map
                and partial_romnum in decoding_map):
            running_total += int(decoding_map[partial_romnum])
            partial_romnum = ''
        partial_romnum += romnum_letter
    running_total += int(decoding_map[partial_romnum])

    return running_total


def get_cli_args():

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(
        title='subcommands',
        description='valid subcommands',
        dest='subcommand')

    subparser_encode = subparsers.add_parser('encode')
    subparser_encode.add_argument('integer', type=int)

    subparser_decode = subparsers.add_parser('decode')
    subparser_decode.add_argument('romnum')

    return parser.parse_args()


def main():

    cli_args = get_cli_args()
    if cli_args.subcommand == 'encode':
        print(encode(cli_args.integer))
    elif cli_args.subcommand == 'decode':
        print(decode(cli_args.romnum))


if __name__ == '__main__':
    main()
