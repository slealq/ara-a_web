from datetime import date
from logging import getLogger
from json import dumps, loads
from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from oddcrawler.webpage_extractors import WebpageExtractor


class CRHoyExtractor(WebpageExtractor):

    LOAD_TIMEOUT = 10
    URL_SECTION_TIMEOUT = 1
    PARAGRAPH_TIMEOUT = 1

    def __init__(self):
        self._main_url = 'https://www.crhoy.com/site/dist/ultimas.php'
        self._logger = getLogger(
            'oddcrawler.webpage_extractors.CRHoyExtractor')
        self._driver = Firefox()
        self._datetime_date = date.today()
        self._urls_section_xpath =\
            '/html/body/section/div[1]/div/div/div/div[3]'
        self._urls_xpath =\
            '/html/body/section/div[1]/div/div/div/div[3]/div[{number}]/a'

    def __wait_until_page_loads(self, xpath, timeout=None):
        """Wait unitl LOAD_TIMEOUT seconds has passed, to confirm there's
        the xpath of the section that contains the news. If it isn't present,
        raise a TimeuutException."""

        if timeout is None:
            timeout = self.LOAD_TIMEOUT

        WebDriverWait(self._driver, timeout).until(
            EC.presence_of_element_located((
                By.XPATH, xpath)))

    def get_news_urls(self, datetime_date):

        self.news_urls = []

        self._driver.get(self._main_url)

        date_form = [input for input in
                     self._driver.find_elements_by_tag_name(
                         'input') if input.get_attribute('id') == 'fecha']

        # There should be only one input with id == 'fecha'
        assert len(date_form) == 1

        # Get the news from asked date
        super(
            CRHoyExtractor,
            self
        )._get_day_month_year_from_datetime(datetime_date)

        self._logger.info('Fetch urls from date {day}/{month}/{year}'.format(
            day=self._day,
            month=self._month,
            year=self._year))

        # Fill the date form with correct information
        date_form = date_form.pop()
        date_form.clear()
        date_form.send_keys('{year}-{month}-{day}'.format(year=self._year,
                                                          month=self._month,
                                                          day=self._day))
        # Wait until page loads
        try:
            self.__wait_until_page_loads(self._urls_section_xpath)
            self._logger.info('Page loaded succesfully')
        except TimeoutException:
            self._logger.error('Page never fully loaded')

        # Try to grab next news, by xpath. If timeout exists, assume
        # it is because that's the end.
        exception_thrown = False
        news_index = 1
        while not exception_thrown:
            try:
                self._logger.info(
                    'Looking for news number {index}'.format(
                        index=news_index))

                self.__wait_until_page_loads(
                    self._urls_xpath.format(number=news_index),
                    self.URL_SECTION_TIMEOUT
                )

                link_a = self._driver.find_element_by_xpath(
                    self._urls_xpath.format(
                        number=news_index)).get_attribute('href')

                self.news_urls.append(link_a)

                news_index += 1

            except TimeoutException:
                self._logger.info(
                    'Got {news_number} news. Is that right?'.format(
                        news_number=news_index-1))

                exception_thrown = True

        return self.news_urls

    def extract_text_from_news(self):

        self._complete_news_info = {}

        self._paragraph_xpath =('/html/body/div[1]/div[2]/section/div[3]/'
                                'article[1]/div[3]/p[{number}]')

        for each_new_url in self.news_urls:
            self._logger.info(
                'Extract data from {url}'.format(url=each_new_url))

            self._driver.get(each_new_url)
            exception_thrown = False
            paragraph_index = 1
            paragraphs = []
            while not exception_thrown:
                try:
                    self.__wait_until_page_loads(
                        self._paragraph_xpath.format(number=paragraph_index),
                        self.PARAGRAPH_TIMEOUT
                    )

                    paragraphs.append(self._driver.find_element_by_xpath(
                        self._paragraph_xpath.format(
                            number=paragraph_index)).text)

                    paragraph_index += 1

                except TimeoutException:
                    exception_thrown = True

            self._complete_news_info[each_new_url] = ' '.join(paragraphs)

        # Just in case we are running with set on force urls
        # Define day, month and year, with the date defined at build time
        # in __init__.
        super(
            CRHoyExtractor,
            self
        )._get_day_month_year_from_datetime(self._datetime_date)

        # Write self._complete_news_info to a file, with current date.
        with open('complete_news_of_cr_hoy_from_{day}_{month}_{year}.json'
                  ''.format(day=self._day,
                            month=self._month,
                            year=self._year), 'w') as f:
            f.write(dumps(self._complete_news_info))
            f.close()

        return self._complete_news_info

    def filter_news_by_keywords(self, keywords: list) -> dict:
        """Given the complete information from news, return a dictionary
        that only contains news in which the text contains one of the
        keywords asked for."""

        self._logger.info(
            'Appling filters to info using this keywords: {keywords}'.format(
                **locals()))

        self._filtered_news_info = {'keywords': keywords}

        for key, value in self._complete_news_info.items():
            match = False
            for each_keyword in keywords:
                # Only one match is enough
                if each_keyword.lower() in value.lower():
                    match = True
                    break

            if match:
                self._logger.info('Hit found with {url}'.format(url=key))
                self._filtered_news_info[key] = value

        # Just in case we are running with set on force urls
        # Define day, month and year, with the date defined at build time
        # in __init__.
        super(
            CRHoyExtractor,
            self
        )._get_day_month_year_from_datetime(self._datetime_date)

        # Write the filtered result in disk
        with open('filtered_news_of_cr_hoy_from_{day}_{month}_{year}.json'
                  ''.format(
                      day=self._day,
                      month=self._month,
                      year=self._year), 'w') as f:
            f.write(dumps(self._filtered_news_info))
            f.close()

        return self._filtered_news_info

    def __del__(self):
        self._driver.quit()
