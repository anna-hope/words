#!/usr/bin/env python3.3

import sys, argparse, os, time
import multiprocessing as mp
import simplejson as json
# from langtools import seq_freqs

def get_lang_data(filename=None):
    if filename is None:
        filename = args.fn
        
    if not filename.endswith('.json'):
        filename = filename + '.json'
        
    if os.path.exists(filename):
        lang_data = json.load(open(filename))
    else:
        lang_data = {'sequences': {}}
    
    return lang_data

def dump_data(lang_data, filename=None):
    if filename is None:
        filename = args.fn
        
    if not filename.endswith('.json'):
        filename = filename + '.json'
    
    file = open(filename, 'w')
    json.dump(lang_data, file)
    file.close()

def seq_freqs(words, seq_length):
    sequences = []
    
    for word in words:
        for i in range(len(word) - (seq_length - 1)):
            sequence = word[i:i+seq_length]
            if len(sequence) == seq_length:
                sequences.append(sequence)
                
    seq_set = set(sequences)
    
    seqs_frequencies = {seq: (sequences.count(seq) / len(sequences)) for seq in seq_set}
    print('Done {}-letter sequences'.format(seq_length))
    return seq_length, seqs_frequencies
    
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

def process_sequence(result):
    lang_data = get_lang_data()
    lang_data['sequences'][result[0]] = result[1]
    dump_data(lang_data)
        
def main():
    print('Working...')
    
    begin_time = time.time()
    
    lang_data = get_lang_data()
    
    # get words and initial letters
    words, initial_letters = process_words(open(args.fn))
    lang_data['words'] =  words
    lang_data['initial_letters'] = initial_letters
    dump_data(lang_data)

    print('Got words and initial letters, beginning to compute sequences...')
    print('Go get a cuppa and a sandwich, this will take a while...')
    
    with mp.Pool(processes=args.maxseqlength, maxtasksperchild=1) as p:
        results = []
        sequences = {}
        for i in range(args.maxseqlength):
            seq_length = i + 1
            print('Doing {} letter sequences'.format(seq_length))
            r = p.apply_async(seq_freqs, args=(words, seq_length), callback=process_sequence)
            results.append(r)
            
        for r in results:
            r.wait()
        
    delta = time.time() - begin_time
    print('Finished processing in {} minutes'.format(round(delta / 60)))
            
    
    
if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('fn', type=str, help='Word file to analyse')
    argparser.add_argument('--maxseqlength', type=int, default=4, 
                                help='maximum sequence length to analyse')
    argparser.add_argument('--onlymax', action='store_true', default=False,
                                        help='only analyse the maximum length provided')
    args = argparser.parse_args()
    
    main()