#!/usr/bin/env python3

"""Quick util to read beer glossary terms from a CSV file, and pick two of them at random
    to be inserted into a monthly email newsletter. Script will also prevent items being
    picked twice."""


import csv
from datetime import datetime
import random
import os


def load_picked():
    with open('gp.txt', 'r') as f:
        return [x for x in f.readlines()]


def load_glossary():
    glossary = []
    with open('beerglossary.csv', newline='') as csvfile:
        mr_wonky = csv.reader(csvfile, dialect='excel')
        for row in mr_wonky:
            gloss = (row[0], row[1], row[2])
            glossary.append(gloss)
    return glossary


def pick_terms(glossary, picked):
    terms = []
    while len(terms) < 2:
        candidate = random.choice(glossary)
        if candidate[0] not in picked:
            terms.append(candidate)
            picked.append(candidate[0])
    return terms, picked


def output_results(terms):
    folder = os.path.join(os.path.expanduser('~'), 'Documents/beerblog/newsletter')
    my_date = '{:%Y-%m-%d}'.format(datetime.now())
    with open(f'{folder}/glossary_items_{my_date}.txt', 'w') as f:
        for t in terms:
            f.write(f'**{t[1]}** - {t[2]}\n\n')


def store_picked(picked):
    with open('gp.txt', 'w') as f:
        for p in picked:
            f.write(f'{p}\n')


def main():
    picked = load_picked()
    glossary = load_glossary()
    terms, new_picked = pick_terms(glossary, picked)
    output_results(terms)
    store_picked(new_picked)
    print(f'Operation complete. Terms chosen: {terms[0][1]} | {terms[1][1]}')


if __name__ == "__main__":
    main()
