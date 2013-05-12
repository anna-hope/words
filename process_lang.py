#!/usr/bin/env python3.3

import sys, argparse
import simplejson as json
from langtools import seq_freqs

def dump(lang_data, filename=None):
    if filename is None:
        filename = args.fn
    file = open('{}.json'.format(filename), 'w')
    json.dump(lang_data, file)
    file.close()
    
def process_words(words):
    new_words = []
    initial_letters = []
    
    for word in words:
        word = word.strip().casefold()
        if len(word) >= 4:
            new_words.append(word)
            if word[0] not in initial_letters:
                initial_letters.append(word[0])
    
    return new_words, initial_letters

def main():
    print('Working...')
    # we'll be dumping everything into a JSON file along the way
    lang_data = {}
    
    # get words and initial letters
    words, initial_letters = process_words(open(args.fn))
    lang_data['words'] = words
    lang_data['initial_letters'] = initial_letters
    dump(lang_data)
    print('Got words, getting letters...')
    
    symbol_freqs = seq_freqs(words, 1)
    
    # get all symbols in the bank
    all_symbols = [symbol for symbol in symbol_freqs]
    
    lang_data['all_symbols'] = all_symbols
    dump(lang_data)
    print('Got letters...')
    
    print('Calculating sequence frequencies. Go make yourself a hot drink because this will take a while...')
    seq_freqs_3 = seq_freqs(words, 3)
    lang_data['sequences'] = {'3': seq_freqs_3}
    dump(lang_data)
    
    print('Done for three letter sequences. Doing four letter sequences. You might as well go out for a party or whatever, because this usually takes very long...')
    seq_freqs_4 = seq_freqs(words, 4)
    lang_data['sequences']['4'] = seq_freqs_4
    dump(lang_data)
    
    print('Done the frequencies, packing it up...')
    print('Yay, all done!')
    
if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('fn', type=str, help='Word file to analyse')
    args = argparser.parse_args()
    
    main()