#!/usr/bin/env python3.3

import random, argparse
from words import lie



def make_up(seq='', lang='en'):
	for i in range(random.randrange(6, 12)):
		letter = lie(seq, lang=lang)
		if letter is None:
			break
		seq += letter
	return seq
		

def main():
	print(make_up(args.sequence, args.lang))

if __name__ == '__main__':
	ap = argparse.ArgumentParser()
	ap.add_argument('sequence', type=str, help='sequence to begin building a word with')
	ap.add_argument('-l', '--lang', type=str, choices=['en', 'ru'], default='en', help='language to build a word in')
	args = ap.parse_args()
	main()