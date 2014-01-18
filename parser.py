# coding=utf-8

"""Script for choosing the most popular music news based on some heuristics.

Heuristic ideas:

- single word token counts
- two-word token counts
- three-word token counts
- looking for proper nouns, perhaps via strings of capitalized words
- looking for proper nouns, perhaps via a mashup against wikipedia entries
- mashup against last fm band names
"""

import cPickle as pickle
import HTMLParser
import operator
from pprint import pprint
import string

import common


POPULARITY_THRESHOLD = 2

TOKENS_IGNORE = ['a', 'the', 'on', 'of', 'with', 'to', 'in', 'for', 'at', 'and',
    ('of', 'the'),
    ('new', 'song'),
    ('new', 'album'),
    ('touring', 'with'),
    ('album', 'in'),
    ('the', 'week'),
    ('check', 'out'),
    ('and', 'the'),
]

h = HTMLParser.HTMLParser()
strip_text = string.punctuation + u'–' + u'\u201c' + u'\u201d'


def get_entries():
    with open(common.FILENAME_DATA, 'r') as fp:
        return pickle.load(fp)


def heuristic1(entries):
    def tokenize(text):
        tokens = text.split(' ')
        #last_token = None
        for token in tokens:
            token = h.unescape(token)
            token = token.lower().strip(strip_text)
            if token:
               yield token
            # if token and last_token:
            #     yield (last_token, token)
            # last_token = token

    words = {}
    for entry in entries:
        #print entry['title']
        for token in tokenize(entry['title']):
            if token in TOKENS_IGNORE:
                continue
            #print "\t%s" % token
            if token not in words:
                words[token] = []
            words[token].append(entry)
    popularity = {key: len(value) for key, value in words.iteritems()}
    sorted_popularity = sorted(popularity.iteritems(), key=operator.itemgetter(1), reverse=True)
    
    popular = {}
    for item in sorted_popularity:
        token, popularity = item
        if popularity <= POPULARITY_THRESHOLD:
            break
        print "%s (%s)" % (token, popularity)
        for entry in words[token]:
            key = entry['link']
            if key not in popular:
                popular[key] = entry
            print "\t%s" % h.unescape(entry['title'])
            print "\t%s" % entry['link']
            print ""


def main():
    entries = get_entries()
    heuristic1(entries)

if __name__ == '__main__':
    main()
