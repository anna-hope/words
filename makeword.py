#!/usr/bin/env python3.3

import random, argparse
from words import lie
try:
	import simplejson as json
except ImportError:
	import json

def make_up(lang_data, seq=''):
	for i in range((12 - len(seq))):
		letter = lie(seq, lang_data)
		if letter is None:
			break
		seq += letter
	return seq

def main():
	lang_data = json.load(open('{}.json'.format(args.lang)))
	print(make_up(lang_data, args.sequence))

if __name__ == '__main__':
	ap = argparse.ArgumentParser()
	ap.add_argument('sequence', type=str, help='sequence to begin building a word with')
	ap.add_argument('-l', '--lang', type=str, choices=['en', 'ru', 'de'], default='en', help='language to build a word in')
	args = ap.parse_args()
	main()