#!/usr/bin/env python3

from datetime import date
from oddcrawler.webpage_extractors import monumental_extractor
from logging import (getLogger, FileHandler, StreamHandler, Formatter, DEBUG,
                     ERROR)


def test_get_news_urls(webpage_extractor):
    urls = webpage_extractor.get_news_urls(date.today())
    assert isinstance(urls, list)


if __name__ == "__main__":
    # Configure logger: oddcrawler needsd to be the top logger
    logger = getLogger('oddcrawler')
    logger.setLevel(DEBUG)
    # create file file handler
    fh = FileHandler('extractor_test.log')
    fh.setLevel(DEBUG)
    # create console handler
    ch = StreamHandler()
    ch.setLevel(ERROR)
    # create formatter and add it to handlers
    formatter = Formatter('%(levelname)s %(asctime)-15s %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)

    # Begin first test
    logger.info('Begin Monumental get_news_urls test')
    monumental_extractor = monumental_extractor()
    urls = test_get_news_urls(monumental_extractor)
    print(urls)
    assert isinstance(urls, list)

    # Test for other extractors might go here
