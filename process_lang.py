#!/usr/bin/env python3.3

import sys, argparse
import simplejson as json
from langtools import get_words, seq_freqs

def main():
    print('Working...')
    # we'll be dumping everything into a JSON file along the way
    lang_data = {}
    file = open('{}.json'.format(args.fn), 'w')
    
    # get words
    words = get_words(open(args.fn))
    lang_data['words'] = words
    json.dump(lang_data, file)
    print('Got words, getting letters...')
    
    letter_freqs = seq_freqs(words, 1)
    # get the letters
    letters = [letter for letter in letter_freqs if letter != '-']
    
    lang_data['letters'] = letters
    json.dump(lang_data, file)
    print('Got letters...')
    
    print('Calculating sequence frequencies. Go make yourself a hot drink because this will take a while...')
    seq_freqs_3 = seq_freqs(words, 3)
    lang_data['sequences'] = {'3': seq_freqs_3}
    json.dump(lang_data, file)
    
    print('Done for three letter sequences. Doing four letter sequences. You might as well go out for a party or whatever, because this usually takes very long...')
    seq_freqs_4 = seq_freqs(words, 4)
    lang_data['sequences']['4'] = seq_freqs_4
    json.dump(lang_data, file)
    
    print('Done the frequencies, packing it up...')
    file.close()
    print('Wrote the JSON file...')
    print('Yay, all done!')
    
if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('fn', type=str, help='Word file to analyse')
    args = argparser.parse_args()
    
    main()