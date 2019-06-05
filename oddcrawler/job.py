from timeloop import Timeloop
from datetime import timedelta, datetime
from logging import (getLogger, FileHandler, StreamHandler, Formatter, DEBUG,
                     ERROR)

class ExtractorJob():

    def __init__(self, periodicity, text_filter, source):
        self.periodicity = timedelta(seconds=periodicity)
        self.source = source
        self.text_filter = [text_filter]
        self.t1 = Timeloop()

    def test_function(self):
        self.logger.info('Begin {source_name} test'.format(
            source_name=self.source.__name__))
        print('In test function')

    def target_function(self):
        print('Begin target function')
        # Begin first test
        self.logger.info('Begin {source_name} test'.format(
            source_name=self.source.__name__))
        extractor = self.source()
        # Get the urls
        extractor.get_news_urls(datetime.today())
        # Extract text from news
        extractor.extract_text_from_news()
        # Filter by keywords
        extractor.filter_news_by_keywords(self.text_filter)
        # Close the extractor
        del extractor

    def setup_logger(self):
        # Configure logger: oddcrawler needsd to be the top logger
        self.logger = getLogger('oddcrawler')
        self.logger.setLevel(DEBUG)
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
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def run(self):
        self.setup_logger()
        self.t1._add_job(self.target_function, interval=self.periodicity)
        self.t1.start(block=True)
