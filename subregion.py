#!/usr/bin/env python3

import sys
from regions import load_subregion_codes

if __name__ == '__main__':
    for i in load_subregion_codes(sys.argv[1].upper().removesuffix("*")):
        print(i)