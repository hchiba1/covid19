#!/usr/bin/env python3
import sys
import re
import argparse
from classes.Extractor import Extractor

parser = argparse.ArgumentParser(description='MHLW COVID Info Extractor.')
parser.add_argument('-i', '--input', help='Input URL')
parser.add_argument('-n', '--num', type=int, help='Only a few lines for each table')
parser.add_argument('-j', '--japan', action='store_true', help='Japanese domestic information')
parser.add_argument('-w', '--world', action='store_true', help='World information')
parser.add_argument('-v', '--verbose', action='store_true', help='Verbose')
args = parser.parse_args()

ex = Extractor(args)

if args.input:
    ex.extract_table(args.input, args.num)
    sys.exit()

list = ex.extract_list(args.verbose)

for item in list:
    link = item.get("href")
    ex.extract_table(link, args.num)
