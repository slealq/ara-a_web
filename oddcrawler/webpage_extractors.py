# -*- coding: utf-8 -*-
"""There are four main news source implemented for now: Monumental, La Prensa
 Libre, La Extra y CR Hoy."""

from abc import ABC, abstractmethod
from logging import getLogger
from json import dumps
from datetime import date
from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# create logger
_logger = getLogger('oddcrawler.webpage_extractors')


class WebpageExtractor(ABC):
    LOAD_TIMEOUT = 10
    _WEEKDAY_TRADUCTION = {0: 'Lunes',
                            1: 'Martes',
                            2: 'Miércoles',
                            3: 'Jueves',
                            4: 'Viernes',
                            5: 'Sábado',
                            6: 'Domingo'}

    _MONTH_NUMBER_TRADUCTION = {1: 'enero',
                                2: 'febrero',
                                3: 'marzo',
                                4: 'abril',
                                5: 'mayo',
                                6: 'junio',
                                7: 'julio',
                                8: 'agosto',
                                9: 'septiembre',
                                10: 'octubre',
                                11: 'noviembre',
                                12: 'diciembre'}

    def __init__(self):
        self._main_url = None
        self._logger.info('Starting a new driver using Firefox')
        self._driver = Firefox()
        self._datetime_date = date.today()

    def _get_day_month_year_from_datetime(self, datetime_date):
        self._datetime_date = datetime_date
        self._year = datetime_date.year
        self._month = datetime_date.month
        self._day = datetime_date.day
        self._weekday = datetime_date.weekday()
        self._weekday_name = self._WEEKDAY_TRADUCTION[self._weekday]
        self._month_name = self._MONTH_NUMBER_TRADUCTION[self._month]

    def _wait_until_page_loads(self, xpath, timeout=None):
        """Wait unitl LOAD_TIMEOUT seconds has passed, to confirm there's
        the xpath of the section that contains the news. If it isn't present,
        raise a TimeuutException."""

        if timeout is None:
            timeout = self.LOAD_TIMEOUT

        WebDriverWait(self._driver, timeout).until(
            EC.presence_of_element_located((
                By.XPATH, xpath)))

    @abstractmethod
    def get_news_urls():
        pass

    @abstractmethod
    def extract_text_from_news():
        """Extract main news text from the url. The location of this text
        will be dependent of each newspaper."""
        pass

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
        self._get_day_month_year_from_datetime(self._datetime_date)

        # Write the filtered result in disk
        with open('filtered_news_of_{name}_from_{day}_{month}_{year}.json'
                  ''.format(name=self.NAME,
                            day=self._day,
                            month=self._month,
                            year=self._year), 'w') as f:
            f.write(dumps(self._filtered_news_info))
            f.close()

        return self._filtered_news_info
