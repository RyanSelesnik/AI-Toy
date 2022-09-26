"""
This script is used to preprocess and train the KenLM language model on the  
daily dialogues dataset
"""
import numpy as np
import re
from datasets import load_dataset
import os


def flatten(l):
    return [item for sublist in l for item in sublist]


def extract_text(batch):
    """Removes punctuation and other stuff"""
    chars_to_ignore_regex = '[,?.!\-\;\:"“%‘”�—’…–]'
    return re.sub(chars_to_ignore_regex, "", batch.lower())


dataset = load_dataset('daily_dialog', split='train')
flattened_data = flatten(dataset['dialog'])
# Remove punctuation
processed_data = list(map(extract_text, flattened_data))

with open("text.txt", "w") as file:
    file.write(" ".join(processed_data))

os.system("kenlm/build/bin/lmplz - o 5 < 'text.txt' > '5gram.arpa' ")

with open("5gram.arpa", "r") as read_file, open("5gram_correct.arpa", "w") as write_file:
    has_added_eos = False
    for line in read_file:
        if not has_added_eos and "ngram 1=" in line:
            count = line.strip().split("=")[-1]
            write_file.write(line.replace(f"{count}", f"{int(count)+1}"))
        elif not has_added_eos and "<s>" in line:
            write_file.write(line)
            write_file.write(line.replace("<s>", "</s>"))
            has_added_eos = True
        else:
            write_file.write(line)
