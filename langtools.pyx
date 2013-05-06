#!/usr/bin/env python3.3

# a script to analyse frequencies of letter sequences in a word bank
# (c) Anton Osten

def get_words(input_data):
    # weed out the extraneous data
    words = [word.strip().casefold() for word in input_data if len(word) >= 4]
    return words

def seq_freqs(words, seq_length=4):
    sequences = []
    
    for word in words:
        for i in range(len(word)):
            sequence = word[i:i+seq_length]
            if len(sequence) == seq_length:
                sequences.append(sequence)
    
    seqs_frequencies = {seq: (sequences.count(seq) / len(sequences)) for seq in set(sequences)}
    return seqs_frequencies