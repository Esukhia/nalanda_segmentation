import os
import re
from utils import *

# three punctuation markers need to be addressed: ?, + and -
# the first can be directly deleted, as any of the other non_tibetan, while - needs to be kept, adding a space to make
# it into a separate word.

def separate_punct(string):
    punct = ['༄', '༅', '།', '༑', '༎', '༏', '༐', '༔', '༈']
    separated = ''
    text_chunk = ''
    punct_chunk = ''
    for num, char in enumerate(string):
        if char != ' ':
            if char not in punct:
                # add the punct chunk after modifying it
                if punct_chunk:
                    punct_chunk = punct_chunk.replace(' ', '_')
                    punct_chunk = ' {} '.format(punct_chunk)
                    separated += punct_chunk
                    punct_chunk = ''
                text_chunk += char
            if char in punct:
                # add the text chunk
                if text_chunk:
                    separated += text_chunk
                    text_chunk = ''
                punct_chunk += char
        # deal with the space: add it to the right chunk
        else:
            if num >= 0:
                previous_char = string[num - 1]
            else:
                previous_char = ''
            if num <= len(string)-2:
                next_char = string[num + 1]
            else:
                next_char = ''
            if previous_char in punct or next_char in punct:
                punct_chunk += char
            else:
                text_chunk += char
    return separated

# obtained through build_corpus_lexicon.py
non_tibetan = ['﻿', 'A', 'a', ']', '2', '\\', 'c', 'r', 'e', ',', 'm', '.', 'j', 'n', 'N', 'l', 'b', '=', ')', '8',
               'z', '•', 's', '1', 'h', 'v', 'L', '[', '!', '῝', 'ᨘ', '(', '`', '?', '+']

in_path = 'initial'
out_path = 'cleaned'
for file in os.listdir(in_path):
    content = open_file('{}/{}'.format(in_path, file))
    # replace all the sequences of space characters by a single normal space
    content = re.sub(r'\s+', ' ', content)

    # delete non_tibetan
    for n in non_tibetan:
        content = content.replace(n, '')

    # separate affixed
    content = content.replace('-', ' -')
    # replace non-breaking tseks
    content = content.replace('༌', '་')
    # separate punct
    content = separate_punct(content)
    # delete final tseks in order to have more matching contexts for the alternative segmentations
    content = content.replace('་ ', ' ')

    write_file('{}/{}'.format(out_path, file), content)