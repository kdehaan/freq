# Name: Kevin de Haan
# Section: EB1
# Copied code: N/A

# Resources used: http://pythex.org/, https://pyformat.info/,
# http://www.python-course.eu/python3_dictionaries.php

# Assumptions made:
# Based on the output of the sample i/o file, underscores were considered to be
# punctuation and hyphens were not. Other punctuation was defined as being
# non-alphanumeric and non-whitespace. This may be easily changed by editing the
# regex for replacements. Formatting was designed to be as similar as possible to
# the example but may vary slightly.


import sys
import argparse
import re


parser = argparse.ArgumentParser(
    description='Sort a text file.',
    formatter_class=argparse.RawTextHelpFormatter,
    )

parser.add_argument("-i", "--ignore-case",
    help="ignore letter case when sorting",
    action="store_true",
    dest="ignore_case")

parser.add_argument("--de-hyphen",
    help="de-hyphenate words that end in - and break over lines",
    action="store_true",
    dest="de_hyphen")

parser.add_argument("--remove-punct",
    help="throws away any punctuation in a word",
    action="store_true",
    dest="remove_punct")

parser.add_argument("--pairs",
    help="instead of counting single words, count ordered pairs of words",
    action="store_true",
    dest="pairs")

parser.add_argument("--sort",
    help="""\
Options:
byfreq - print a frequency table sorted by frequency in decreasing frequency order
byword - print a frequency table sorted by word in increasing lexicographical order
""",
    nargs='?',
    choices=['byfreq', 'byword'],
    default='byfreq',
    dest="sort_type")


parser.add_argument("infile",
    help="file to be sorted, stdin if omitted",
    nargs="?",
    type=argparse.FileType('r'),
    default=sys.stdin)


args = parser.parse_args()

words = {}

prevLine = ''
prevWord = ''

#primary function for adding keys to the words{} dictionary
def splitWords(args, words, prevWord, line):
    for word in line.split():
        key = word
        if args.pairs:
            if prevWord == '':
                prevWord = word
                continue
            key = prevWord + ' ' + word
        words[key] = words.get(key, 0) + 1
        prevWord = word
    return prevWord

# fetch all the lines
for line in args.infile:
    line = line.strip()

    if args.ignore_case:
        line = line.lower()
    if args.remove_punct:
        line = re.sub("[^\w\s-]", "", line) #removes all punct except '-'
        line = re.sub("[_]", "", line) #removes underscores
    if len(line) == 0:
        continue
    if args.de_hyphen & (line[-1] == "-"):
        prevLine += line[0:-1:1]
    else:
        line = (prevLine + line)
        prevLine = ''
        prevWord = splitWords(args, words, prevWord, line)

# Captures words if last line is hyphenated
if prevLine != '':
    splitWords(args, words, prevWord, prevLine+'-')

totalWords = 0
for key in words:
    totalWords += words[key]
    words[key] = [words[key]] #turns dictionary entries into a list

for key in words: #adds new index to the dictionary list
    words[key].append(words[key][0]/totalWords)

if args.sort_type == "byword":
    for key in sorted(words):
        print("{0:7s} {1:3d} {2:>11.7f}".format(key, words[key][0], words[key][1]))
else: #sorting twice like this works because sorted() is guaranteed to sort in place
    for key in sorted(sorted(words.items()), key=lambda L: L[1][1], reverse=True):
        print("{0:7s} {1:3d} {2:>11.7f}".format(key[0], key[1][0], key[1][1]))
