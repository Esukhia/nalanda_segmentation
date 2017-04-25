import os
from collections import defaultdict
import re
from utils import *


def is_tibetan_letter(char):
    """
    :param char: caracter to check
    :return: True or False
    """
    if (char >= 'ༀ' and char <= '༃') or (char >= 'ཀ' and char <= 'ྼ'):
        return True
    else:
        return False


def non_tib_chars(string):
    """
    :param string:
    :return: list of non-tibetan non-tibetan-pre_process characters found within a orig_list
    """
    punct = ['༄', '༅', '།', '་', '༌', '༑', '༎', '༏', '༐', '༔', '༈', '-', '_']
    chars = []
    for character in string:
        if not is_tibetan_letter(character) and character not in chars and character not in punct:
            chars.append(character)
    return chars


def find_corpus_non_tib(file_list):
    all_non_tib = defaultdict(int)
    for f in file_list:
        content = open_file(f).strip().split()
        for c in content:
            non_tib = non_tib_chars(c)
            for n in non_tib:
                all_non_tib[n] += 1
    write_file('non_tib_characters.txt', '\n'.join(['{}: {}'.format(k, v) for k, v in all_non_tib.items()]))
    return all_non_tib


def extract_vocab_with_freq(files_list):
    total = defaultdict(int)
    non_tib_total = find_corpus_non_tib(files_list)
    for f in files_list:
        content = open_file(f).strip().split()
        for c in content:
            clean = c
            for a in non_tib_total:
                clean = clean.replace(a, '')
            clean = re.sub(r'^[༌་༄༅།༑༔\s\t]*(.*)[༌་༄༅།༑༔\s\t]*$', r'\1', clean)
            total[clean] += 1
    return total


def compare_lists(base_list, to_compare_list):
    base = extract_vocab_with_freq(base_list)
    to_compare = extract_vocab_with_freq(to_compare_list)

    only_in_to_compare = []
    shared_words = []
    for word in to_compare:
        if word not in base:
            only_in_to_compare.append(word)
        else:
            shared_words.append(word)
    return only_in_to_compare, shared_words


def main():
    raw_corpus_path = './cleaned'
    raw_corpus_files = ['{}/{}'.format(raw_corpus_path, a) for a in os.listdir(raw_corpus_path)]
    corpus_vocab = extract_vocab_with_freq(raw_corpus_files)
    write_file('corpus_vocab_tib_order.txt', '\n'.join(tib_sort(corpus_vocab)))
    freq_sorted = sorted([(k, v) for k, v in corpus_vocab.items()], key=lambda x: x[1], reverse=True)
    write_file('corpus_vocab_freq_order.txt', '\n'.join(['{},{}'.format(a[0], a[1]) for a in freq_sorted]))

main()