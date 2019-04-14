#!/usr/bin/env python3

from datetime import date
from oddcrawler.webpage_extractors import monumental_extractor
from logging import (getLogger, FileHandler, StreamHandler, Formatter, DEBUG,
                     ERROR)


def test_get_news_urls(webpage_extractor):
    urls = webpage_extractor.get_news_urls(date.today())
    assert isinstance(urls, list)

    return urls

def test_extract_text_from_news(webpage_extractor):
    """Needs `get_news_urls` to have been run first. Otherwise, assertion
    of news_urls will fails.

    It's expected that the result is a dictionary, and it contains urls
    as keys and text of the news as values.
    """

    assert isinstance(webpage_extractor.news_urls, list) \
        and webpage_extractor.news_urls

    text = webpage_extractor.extract_text_from_news()

    assert isinstance(text, dict)

    return text

def test_filter_news_by_keywords(webpage_extractor):
    filtered_news = webpage_extractor.filter_news_by_keywords(
        ['registro', 'especie', 'Gobierno'])

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
    test_get_news_urls(monumental_extractor)
    # print(urls)

    # Test the text extraction
    test_extract_text_from_news(monumental_extractor)

    # Test for filtered by keywords
    test_filter_news_by_keywords(monumental_extractor)

    # Test for other extractors might go here
