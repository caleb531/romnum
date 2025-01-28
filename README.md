# romnum

*Copyright 2021-2025 Caleb Evans*  
*Released under the MIT license*

[![tests](https://github.com/caleb531/romnum/actions/workflows/tests.yml/badge.svg)](https://github.com/caleb531/romnum/actions/workflows/tests.yml)
[![Coverage Status](https://coveralls.io/repos/caleb531/romnum/badge.svg?branch=main)](https://coveralls.io/r/caleb531/romnum?branch=main)

This package is a Python 3 CLI utility for converting to and from Roman
numerals.

Please note that the Roman numeral overbar notation (for multiplying by 1,000)
is not supported.

## Usage

### Installation

```sh
pip3 install romnum
```

### Encoding

```sh
romnum encode 1776
# MDCCLXXVI
```

### Decoding

```sh
romnum decode MDCCLXXVI
# 1776

```
