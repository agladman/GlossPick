#!/usr/bin/env python3

"""Quick util to read beer glossary terms from a CSV file, and pick two of them at random
    to be inserted into a monthly email newsletter. Script will also prevent items being
    picked twice."""


import csv
from datetime import datetime
import random
import os


BASEDIR = os.path.dirname(os.path.abspath(__file__))
LOGFILE = os.path.join(BASEDIR, 'gp.txt')
CSVFILE = os.path.join(BASEDIR, 'beerglossary.csv')


def load_picked():
    with open(LOGFILE, 'r') as f:
        raw = f.readlines()
        return [r.strip('\n') for r in raw]


def load_glossary():
    glossary = []
    with open(CSVFILE, newline='') as csvfile:
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
    with open(LOGFILE, 'w') as f:
        for p in picked:
            if p is not '':
                f.write(p + '\n')


def main():
    picked = load_picked()
    glossary = load_glossary()
    terms, new_picked = pick_terms(glossary, picked)
    # output_results(terms)
    store_picked(new_picked)
    print(f'''\nOperation complete. Terms chosen:
            \n\t{terms[0][1]} - {terms[0][2]}
            \n\t{terms[1][1]} - {terms[1][2]}\n''')


if __name__ == "__main__":
    main()
