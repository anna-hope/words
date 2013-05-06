#!/usr/bin/env python3.3

import sys, argparse
import simplejson as json
from langtools import get_words, seq_freqs

def main():
    print('Working...')
    words = get_words(open(args.fn))
    print('Got words, getting letters...')
    
    letter_freqs = seq_freqs(words, 1)
    # get the letters
    letters = [letter for letter in letter_freqs if letter != '-']
    print('Got letters...')
    
    print('Calculating sequence frequencies. Go make yourself a hot drink because this will take a while...')
    seq_freqs_3 = seq_freqs(words, 3)
    print('Done for three letter sequences. Doing four letter sequences. Get yourself another hot drink...')
    seq_freqs_4 = seq_freqs(words, 4)
    
    print('Done the frequencies, packing it up...')
    
    # assemble the language data
    lang_data = {'words': words, 'letters': letters, 'sequences': {
    '3': seq_freqs_3, '4': seq_freqs_4}}
    
    # dump it into a JSON file
    file = open('{}.json'.format(args.fn), 'w')
    json.dump(lang_data, file)
    file.close()
    print('Did JSON dump...')
    print('Yay, all done!')
    
if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('fn', type=str, help='Word file to analyse')
    args = argparser.parse_args()
    
    main()