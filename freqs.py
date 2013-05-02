#!/usr/bin/env python3.3

# a script to analyse frequencies of letter sequences in a word bank
# (c) Anton Osten

import sys, pprint, argparse
import simplejson as json

argparser = argparse.ArgumentParser()
argparser.add_argument('fn', type=str, help='Word file to analyse')
argparser.add_argument('-sl', type=int, default=2, help='Sequence length')
argparser.add_argument('-ntp', type=int, default=15, help='Number of most common frequencies to show in output')
args = argparser.parse_args()

def main():
    pp = pprint.PrettyPrinter()
    
    print('Working...')
    words = [word.strip().casefold() for word in open(args.fn) if len(word) >= 4]
    print('Got words...')
    sequences = []
    
    for word in words:
        for i in range(len(word)):
            sequence = word[i:i+args.sl]
            if len(sequence) == args.sl:
                sequences.append(sequence)
    
    print('Got sequences...')
    seqs_frequencies = {seq: (sequences.count(seq) / len(sequences)) for seq in set(sequences)}
    print('Got the frequency of sequences...')
    
    # dump them into a JSON file
    seqs_freqs_file = open('seqs_freqs_{}.json'.format(args.fn.replace('/', '_') + str(args.sl)), 'w')
    json.dump(seqs_frequencies, seqs_freqs_file)
    seqs_freqs_file.close()
    print('Did JSON dump...')

    sorted_sf = sorted(seqs_frequencies.items(), key=lambda x: x[1], reverse=True)
    print('Sorted them...')
    top_seqs = [sorted_sf[i] for i in range(args.ntp)]
    print('Top {}:'.format(args.ntp))
    pp.pprint(top_seqs)
    print('Done.')

if __name__ == '__main__':
    main()