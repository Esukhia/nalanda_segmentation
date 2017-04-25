import os
import re
from utils import *
from collections import defaultdict

vocab = open_file('corpus_vocab_freq_order.txt').strip().split('\n')
vocab = [tuple(a.split(',')) for a in vocab]

context_syl_num = 5  # value should be >= 1
in_path = 'cleaned'
per_volume_path = 'output/per_volume'


for file in os.listdir(in_path):
    print(file)
    work_name = file.replace('.txt', '')
    content = open_file('{}/{}'.format(in_path, file))
    counter = 1
    for word, freq in vocab:
        word_regex = word.replace('་', '་\s?')+'\s?'
        context = '([^\s]+\s)?'*context_syl_num
        word_regex = context + '(' + word_regex + ')' + context
        concs = re.findall(word_regex, content)

        # in case there are less elements than expected by the context regex, the first syllables will match, the others become empty elements in the list.
        # pull all the empty elements on the front
        for c in range(len(concs)):
            element = list(concs[c])
            if element[1] == '':
                start = [element[0]]
                del element[0]
                while element and element[0] == '':
                    start = [element[0]] + start
                    del element[0]
                element = start + element
            concs[c] = element

        output = [[' '.join(a[context_syl_num-1:len(a)-context_syl_num+1])]+list(a)+[file]+[' '.join(a)] for a in concs]
        write_file('output/per_volume/{}_{}.tsv'.format(str(counter)+' '+word, work_name), '\n'.join(['\t'.join(a) for a in output]))
        counter += 1


word_total = defaultdict(str)
for file in os.listdir(per_volume_path):
    w = re.sub(r'[a-zA-Z\.\s]+_?', r'', file)
    word_total[w] += open_file('{}/{}'.format(per_volume_path, file))

for word, matches in word_total.items():
    write_file('output/total/{}_conc_total.txt', matches[word])
