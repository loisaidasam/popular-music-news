
import cPickle as pickle
import datetime
import logging
import time

import feedparser


URL_FEEDSPOT_RSS = 'http://www.feedspot.com/folder/4hvNuV8f/rss'
FILENAME_RECENT = 'data.p'
SLEEPTIME_SECS = 60 * 15 # 15 mins


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

fh = logging.FileHandler('downloader.log')
fh.setLevel(logging.INFO)
fh.setFormatter(formatter)

logger.addHandler(ch)
logger.addHandler(fh)


def download():
    try:
        with open(FILENAME_RECENT, 'r') as fp:
            data = pickle.load(fp)
    except IOError:
        logger.warning("IOError while trying to load old data")
        data = []
    logger.info("%s entries loaded from old data", len(data))

    new_entries = feedparser.parse(URL_FEEDSPOT_RSS)['entries']
    logger.info("%s entries found in RSS", len(new_entries))
 
    if not data:
        data = list(reversed(new_entries))
        added = len(data)
    else:
        last_entry = data[-1]
        go = False
        added = 0
        for entry in reversed(new_entries):
            if last_entry['id'] == entry['id']:
                go = True
            elif go:
                data.append(entry)
                added += 1

    # TODO: remove older entries (maybe > 36 hours old?)

    with open(FILENAME_RECENT, 'w') as fp:
        pickle.dump(data, fp)
        logger.info("Successfully wrote %s entries to file", len(data))
    logger.info("%s new entries added", added)


def main():
    while True:
        download()
        logger.info("Sleeping for %0.2f minutes...", 1.0 * SLEEPTIME_SECS / 60)
        time.sleep(SLEEPTIME_SECS)
        logger.info("Woke up")


if __name__ == '__main__':
    main()

