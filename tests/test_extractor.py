#!/usr/bin/env python3

from datetime import date, datetime
from oddcrawler import (MonumentalExtractor, CRHoyExtractor,
                        LaPrensaLibreExtractor, LaRepublicaExtractor)
from logging import (getLogger, FileHandler, StreamHandler, Formatter, DEBUG,
                     ERROR)


def test_get_news_urls(webpage_extractor):
    # urls = webpage_extractor.get_news_urls(date.today())
    urls = webpage_extractor.get_news_urls(datetime(2019, 4, 17))
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
        ['accidente', 'moto', 'choque', 'amputado'])

def complete_test_for_monumental():
    # Begin first test
    logger.info('Begin Monumental test')
    monumental_extractor = MonumentalExtractor()
    test_get_news_urls(monumental_extractor)

    # Test the text extraction
    test_extract_text_from_news(monumental_extractor)

    # Test for filtered by keywords
    test_filter_news_by_keywords(monumental_extractor)

    del monumental_extractor

def complete_test_for_cr_hoy():
    logger.info('Begin CR Hoy test')
    cr_hoy_extractor = CRHoyExtractor()
    test_get_news_urls(cr_hoy_extractor)

     # Test the text extraction
    test_extract_text_from_news(cr_hoy_extractor)

    # Test filtering
    test_filter_news_by_keywords(cr_hoy_extractor)

    del cr_hoy_extractor

def complete_test_for_la_prensa_libre():
    # Begin test
    logger.info('Begin La Prensa Libre test')
    la_prensa_libre = LaPrensaLibreExtractor()
    test_get_news_urls(la_prensa_libre)

    # Test the text extraction
    test_extract_text_from_news(la_prensa_libre)

    # Test filtering
    test_filter_news_by_keywords(la_prensa_libre)

    del la_prensa_libre

def complete_test_for_la_republica():
    # Begin test
    logger.info('Begin La Repúlica test')
    la_republica = LaRepublicaExtractor()

    test_get_news_urls(la_republica)

    # Test text extraction
    test_extract_text_from_news(la_republica)

    # Test filtering
    test_filter_news_by_keywords(la_republica)

    del la_republica

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

    complete_test_for_la_republica()
    complete_test_for_monumental()
    complete_test_for_cr_hoy()
    complete_test_for_la_prensa_libre()
