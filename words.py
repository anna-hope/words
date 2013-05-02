#!/usr/bin/env python3.3

# (c) Anton Osten
# 

import sys, random, argparse, pickle
try:
    import simplejson as json
except ImportError:
    import json

argparser = argparse.ArgumentParser()
argparser.add_argument('-l', '--lang', type=str, default='en', choices=['en', 'ru'], help='language')
argparser.add_argument('-d', '--dev', action='store_true', default=False, help='dev mode')
args = argparser.parse_args()

def lie(sequence, words=None, lang=args.lang):
    chunk = sequence[-2:]
    sequences = json.load(open('seq_{}.json'.format(lang)))
    matches = {x: sequences[x] for x in sequences if x[:len(chunk)] == chunk and '-' not in sequences[x]}
    if matches == {}:
        return None

    best_match = sorted(matches.items(), key=lambda x: x[1], reverse=True)[0]
    if len(sequence) >= 2:
        letter = best_match[0][2]
    else:
        letter = best_match[0][len(sequence)]
    return letter


def get_words(lang=args.lang):
    try:
        wordsfile = pickle.load(open('words_{}'.format(lang), 'rb'))
    except FileNotFoundError:
        sys.exit('Dictionary file not found. Quitting...')
   
    words = [word for word in wordsfile if len(word.strip()) >= 4 and '-' not in word]
    return words

def add_word(word):
    word = word.strip().casefold()
    # don't want random yos messing up our dictionary
    if 'ё' in word:
        word.replace('ё', 'е')

    words = get_words
    words.append(word)
    words.sort()
    file = open('words_{}'.format(args.lang), 'wb')
    pickle.dump(words, file)
    file.close()

def computer_first():
    if random.random() > 0.5:
        return True
    else:
        return False

def get_letter(sequence, words):
    # we could just get matches
    matches = [word for word in words if word.startswith(sequence)]
    # but that would be too boring, wouldn't you say?
    # so let's add some randomness
    random_matches = [word for word in matches if random.random() > random.random() or random.random() < random.random()] # around 0.25 words will be thrown away like this
    if random_matches == []:
        return (None, None)
    match = sorted(random_matches, key=len, reverse=True)[0]
    try:
        letter = match[len(sequence)]
    except IndexError:
        return (None, None)

    assert matches is not None
    return letter, matches

def check_letter(sequence, letter, words):
    matches = [word for word in words if word.startswith(sequence + letter)]
    if matches == []:
        return False, None
    else:
        assert matches is not None
        return True, matches

def is_complete(sequence, words):
    try:
        match = [word for word in words if word == sequence][0]
    except IndexError:
        return False
    else:
        if len(sequence) >= 6:
            return True
        else:
            return False

def call_bluff(sequence, letter='', player='player'):
    words = get_words()
    matches = [word for word in words if word.startswith(sequence + letter)]
    if player == 'player':
        if args.dev:
            print('Am I missing an actual word? I am going to blindly trust you here')
            answer = input('\n')
            if answer == 'y' or answer == 'yes':
                word = input('Tell me that word, please\n')
                if len(word) >= 4:
                    print("Thanks, I'll make sure to remember it.")
                    add_word(word)
                    return True
                else:
                    return False
            else:
                print('Okay then')
                return False
        print('I\'m calling your bluff, dear.')
        if matches == [] and random.random() > 0.5:
            print('I am positive that there is no word with that sequence of letters in common usage. And trust me, I know a lot of words.')
            return False
        else:
            print('Tell me the word you\'re thinking of')
            word = input()
            new_sequence = word[:(len(word)-1)]
            letter = word[len(word)-1]
            valid = check_letter(new_sequence, letter, words)[0]
            if not valid or word[:len(sequence)] != sequence:
                print('No, I don\'t think so')
                return False
            else:
                print('Oh, didn\'t think of that one...')
                return True
    else:
        # this is for later
        if matches == []:
            print('All right, you got me.')
            return False
        else:
            print(matches[0])
            return True

def play(comp_first, lang='en'):
    words = get_words()
    sequence = ''
    cur_player = 'computer' if comp_first else 'player'
    
    while True:
        if cur_player == 'computer':
            letter, words = get_letter(sequence, words)
            if letter is None:
                letter = lie(sequence)
                words = get_words()
            assert words is not None
            sequence += letter
            print(letter, end='')
            if is_complete(sequence, words):
                break
            cur_player = 'player'
        else:
            letter = input('\n').casefold()
            if letter == '':
                continue
            elif letter == 'bluff' or letter == 'блеф':
                bluff = call_bluff(sequence, player='computer')
                if not bluff:
                    cur_player = 'computer'
                break
            else:
                # this is to make sure that no one attempts to enter a bunch of letters at once
                letter = letter[0]
            valid, words = check_letter(sequence, letter, words)
            if valid:
                complete = is_complete(sequence, words)
                if complete:
                    break
                sequence += letter
                cur_player = 'computer'
            else:
                if call_bluff(sequence, letter):
                    cur_player = 'computer'
                break
    print()
    if cur_player == 'computer':
        print('You win.')
    else:
        print('I win.')

def main():
    print('word game --- if you think the computer is making stuff up (and it can), enter bluff to check')
    comp_first = computer_first()
    if comp_first:
        print('I start')
    else:
        print('Enter a letter')
    play(comp_first, args.lang)

if __name__ == '__main__':
    main()