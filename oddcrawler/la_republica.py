from logging import getLogger
from json import dumps
from selenium.common.exceptions import TimeoutException
from oddcrawler.webpage_extractors import WebpageExtractor


class LaRepublicaExtractor(WebpageExtractor):
    NAME = 'la_republica'
    URL_SECTION_TIMEOUT = 1
    NEWS_SECTION_TIMEOUT = 2
    PARAGRAPH_TIMEOUT = 1

    def __init__(self):
        self._logger = getLogger(
            'oddcrawler.webpage_extractors.LaRepublicaExtractor')
        super(LaRepublicaExtractor, self).__init__()

        self._main_url =\
            'https://www.larepublica.net/seccion/ultima-hora?page={number}'
        self._urls_section_xpath =\
            '/html/body/div/div/div[2]/div/section/div/div[1]'
        self._urls_xpath = ('/html/body/div/div/div[2]/div/section/div/div[1]'
                            '/section/article[{number}]')
        self._links_xpath = ('/html/body/div/div/div[2]/div/section/div/div[1]'
                             '/section/article[{number}]/div/div[2]/a')
        self._articles_date = '{weekday} {day} {month_name}, {year}'

    def _hit_page(self, page_number):
        try:
            self._entry_url = self._main_url.format(number=page_number)
            self._driver.get(self._entry_url)
            self._wait_until_page_loads(self._urls_section_xpath)
        except TimeoutException:
            self._logger.info('Page not found. Time out')

    def get_news_urls(self, datetime_date):
        self._get_day_month_year_from_datetime(datetime_date)
        self.news_urls = []

        page_number = 1
        counter  = 0
        found_first_article_that_matches_date = False
        found_last_article_that_matches_date = False

        # Fetch the first page
        self._logger.info(
                'Fetch urls from date {day}/{month}/{year}'.format(
                    day=self._day,
                    month=self._month,
                    year=self._year))
        self._hit_page(page_number)
        self._logger.info('Entry point: {entry_url}'.format(
            entry_url=self._entry_url))

        # Expected date built from datetime_date
        expected_date = self._articles_date.format(
            weekday=self._weekday_name,
            day=self._day,
            month_name=self._month_name,
            year=self._year)

        self._logger.info(
            'Trying to find {expected_date} in article text'.format(
                **locals()))

        while True:
            # Iterate over each page
            self._logger.info(
                'Hitting page {number}'.format(number=page_number))

            # Look for the first article that matches desired date.
            # Start grabbing urls at that point.
            article_counter = 1
            articles_left_in_this_page = True
            while articles_left_in_this_page:
                # Iterate over each article
                try:
                    self._wait_until_page_loads(
                        self._urls_xpath.format(number=article_counter),
                        self.URL_SECTION_TIMEOUT
                    )
                    article = self._driver.find_element_by_xpath(
                        self._urls_xpath.format(number=article_counter))
                    correct_date =\
                        True if expected_date in article.text else False

                    # Machine state for finding first and last valid article,
                    # that matches the required date and
                    # only appends urls with articles in between
                    if correct_date and \
                       not found_first_article_that_matches_date:
                        found_first_article_that_matches_date= True
                        self._logger.info(
                            'First match at page {page_number}, article '
                            '{article_counter}'.format(**locals()))

                    elif  not correct_date and \
                          found_first_article_that_matches_date:
                        found_last_article_that_matches_date = True
                        self._logger.info(
                            'Last match at page {page_number}, article '
                            '{article_counter}'.format(**locals()))

                        # Break inner while for articles in page
                        break

                    if found_first_article_that_matches_date:
                        link = article.find_elements_by_tag_name(
                            'a')[0].get_attribute('href')
                        self.news_urls.append(link)

                    article_counter += 1

                except TimeoutException:
                    # There are no more articles in this page.
                    articles_left_in_this_page = False

            # Stop grabbing links when articles date is past the desired date.
            if found_last_article_that_matches_date:
                break

            # Go to next page and hit it
            page_number += 1
            self._hit_page(page_number)

        return self.news_urls

    def extract_text_from_news(self):
        self._complete_news_info = {}
        self._article_section_xpath =\
            '/html/body/div/div/div[2]/div/section/div/div[1]/article'

        for each_news_url in self.news_urls:
            self._logger.info('Extract data from {each_news_url}'.format(
                **locals()))

            self._driver.get(each_news_url)

            try:
                self._wait_until_page_loads(
                    self._article_section_xpath,
                    self.PARAGRAPH_TIMEOUT
                )

            except TimeoutException:
                self._logger.info('Failed to load {url}'.format(each_news_url))
                continue

            self._complete_news_info[each_news_url] =\
                self._driver.find_element_by_xpath(
                    self._article_section_xpath).text

        # Write self._complete_news_info to a file, with current date.
        with open('complete_news_of_{name}_from_{day}_{month}_{year}'
                  '.json'.format(
                      name=self.NAME,
                      day=self._day,
                      month=self._month,
                      year=self._year), 'w') as f:
            f.write(dumps(self._complete_news_info))
            f.close()

        return self._complete_news_info

    def __del__(self):
        self._logger.info('Closing browser.')
        self._driver.quit()
