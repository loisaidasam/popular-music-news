# coding=utf-8

import cPickle as pickle
import HTMLParser
import logging
import operator
import string


FILENAME_DATA = 'data.p'
TOKENS_IGNORE = (
    'a', 'the', 'on', 'of', 'with', 'to', 'in', 'for', 'at', 'and',
    ('of', 'the'),
    ('new', 'song'),
    ('new', 'album'),
    ('touring', 'with'),
    ('album', 'in'),
    ('the', 'week'),
    ('check', 'out'),
    ('and', 'the'),
    ('new', 'album', 'in')
)

h = HTMLParser.HTMLParser()


def get_logger(name, logger_filename=None):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    if logger_filename:
        fh = logging.FileHandler(logger_filename)
        fh.setLevel(logging.INFO)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger


def get_entries():
    with open(FILENAME_DATA, 'r') as fp:
        return pickle.load(fp)


def remove_html(text):
    return h.unescape(text)


def strip_text(text):
    text = remove_html(text)
    exclude = string.punctuation + u'–' + u'\u201c' + u'\u201d'
    return text.lower().strip(exclude)


def tokenize(text, token_size=1):
    tokens = text.split(' ')
    last_tokens = []
    for token in tokens:
        token = strip_text(token)
        if not token:
            continue
        last_tokens.append(token)
        result = last_tokens[-1*token_size:]
        if len(result) == token_size:
           yield tuple(result)


def ngram_eval(ngram_size, popularity_threshold):
    entries = get_entries()

    words = {}
    for entry in entries:
        for token in tokenize(entry['title'], ngram_size):
            if token in TOKENS_IGNORE:
                continue
            if token not in words:
                words[token] = []
            words[token].append(entry)

    popularity = {key: len(value) for key, value in words.iteritems()}
    sorted_popularity = sorted(popularity.iteritems(), key=operator.itemgetter(1), reverse=True)
    
    popular = {}
    for item in sorted_popularity:
        token, popularity = item
        if popularity <= popularity_threshold:
            break
        print "%s (%s)" % (token, popularity)
        for entry in words[token]:
            key = entry['link']
            if key not in popular:
                popular[key] = entry
            print "\t%s" % remove_html(entry['title'])
            print "\t%s" % entry['link']
            print ""
