#!/usr/bin/env python3
from oddcrawler import job
from oddcrawler import CRHoyExtractor


PERIODICITY = 5
FILTER_TEXT = 'SOMETEXT'

if __name__ == "__main__":
    myjob = job.ExtractorJob(PERIODICITY, FILTER_TEXT, CRHoyExtractor)
    myjob.run()
