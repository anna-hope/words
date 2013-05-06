#!/usr/bin/env python3.3

# (c) Anton Osten
# 

import sys, random, argparse
try:
    import simplejson as json
except ImportError:
    import json

def load_lang_data(lang):
    try:
       lang_data = json.load(open('{}.json'.format(lang))) 
    except FileNotFoundError:
        sys.exit('Language data not found. Quitting...')
    return lang_data

def lie(sequence, lang_data, words=None, seq_length=4, lang='en'):
    # get the last n (seq_length - 1) letters of the sequence, so that we can find the optimal letter to guess
    chunk = sequence[-(seq_length - 1):] 
    sequences = lang_data['sequences'][str(seq_length)]
    matches = {x: sequences[x] for x in sequences if x[:len(chunk)] == chunk and '-' not in x}
    
    if matches == {}:
        return None

    best_match = sorted(matches.items(), key=lambda x: x[1], reverse=True)[0]
    
    if len(sequence) >= (seq_length - 1):
        letter = best_match[0][seq_length - 1]
    else:
        letter = best_match[0][len(sequence)]
    return letter


def get_words(lang_data):
    '''Returns words from language data'''
    words = [word for word in lang_data['words'] if len(word.strip()) >= 4 and '-' not in word]
    # words = [word for word in lang_data['words'] if '-' not in word]
    return words

def add_word(word):
    word = word.strip().casefold()
    # don't want random yos messing up our dictionary
    if 'ё' in word:
        word.replace('ё', 'е')
    
    # get the language data and add the word to it
    lang_data = load_lang_data(args.lang)
    words = get_words(lang_data)
    words.append(word)
    words.sort()
    lang_data['words'] = words
    # dump the file
    file = open('{}.json'.format(args.lang), 'w')
    json.dump(lang_data, file)
    file.close()

def computer_first():
    if random.random() > 0.5:
        return True
    else:
        return False

def pick_letter(sequence, words):
    '''Picks an optimal letter according to the given sequence'''
    # we could just get matches
    matches = [word for word in words if word.startswith(sequence)]
    # but that would be too boring, wouldn't you say?
    # so let's add some randomness
    random_matches = [word for word in matches if random.random() > random.random() or random.random() < random.random()]
    # around 0.25 words will be thrown away like this
    if random_matches == []:
        return (None, None)
    # but we don't want the computer to be stupid, so let's make it prefer words that lead to its winning (i.e., even number of letters left)
    good_matches = [word for word in random_matches if (len(word) - len(sequence)) % 2 is 0]
    # in case there aren't good matches, let's go back to the random ones
    if good_matches == []:
        good_matches = random_matches

    sorted_matches = sorted(good_matches, key=len, reverse=True)
    # and then let's see that one of those matches won't lead us to a premature game over because there is a shorter full word
    # best_matches = []
    # for word in good_matches:
    #     for i in range((len(sequence) + 1), len(sorted_matches[0])):
    #         if is_complete(word[:i], random_matches):
    #             continue
    #         else:
    #             best_matches.append(word)


    # match = best_matches[0] if best_matches != [] else sorted_matches[0]
    match = sorted_matches[0]

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
        return True

def call_bluff(sequence, words, letter='', player='player'):
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
        if matches == []:
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

def play(comp_first, lang_data):
    all_words = get_words(lang_data)
    cur_words = all_words
    sequence = ''
    cur_player = 'computer' if comp_first else 'player'
    
    while True:
        if cur_player == 'computer':
            # if it's first turn, we want the computer to pick a random letter, no thinking
            if sequence == '':
                letter = random.choice(lang_data['letters'])
            else:
                letter, cur_words = pick_letter(sequence, cur_words)
                if letter is None:
                    letter = lie(sequence, lang_data)
                    cur_words = all_words
           # assert words is not None
            sequence += letter
            print(letter, end='')
            if is_complete(sequence, cur_words):
                break
            cur_player = 'player'
        else:
            letter = input('\n').casefold()
            if letter == '':
                continue
            elif letter == 'bluff' or letter == 'блеф':
                bluff = call_bluff(sequence, all_words, player='computer')
                if not bluff:
                    cur_player = 'computer'
                break
            else:
                # this is to make sure that no one attempts to enter a bunch of letters at once
                letter = letter[0]
            valid, words = check_letter(sequence, letter, cur_words)
            if valid:
                sequence += letter
                complete = is_complete(sequence, cur_words)
                if complete:
                    break
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
    lang_data = load_lang_data(args.lang)
    
    print('word game --- if you think the computer is making stuff up (and it can), enter bluff to check')
    comp_first = computer_first()
    
    if comp_first:
        print('I start')
    else:
        print('Enter a letter')
        
    play(comp_first, lang_data)

if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-l', '--lang', type=str, default='en', choices=['en', 'ru', 'de'], help='language')
    argparser.add_argument('-d', '--dev', action='store_true', default=False, help='dev mode')
    args = argparser.parse_args()

    main()
