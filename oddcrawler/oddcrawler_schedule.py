#!/usr/bin/env python3

from argparse import ArgumentParser
from oddcrawler import NewsFilter, JobMetadata, ExtractorJob
from oddcrawler import(LaRepublicaExtractor, CRHoyExtractor,
                       MonumentalExtractor, LaPrensaLibreExtractor)
from oddcrawler import Database

DATABASE_PATH = 'database.pkl'

EXTRACTOR_MAP = {'la_republica': LaRepublicaExtractor,
                 'cr_hoy': CRHoyExtractor,
                 'monumental': MonumentalExtractor,
                 'la_prensa_libra': LaPrensaLibreExtractor}

PERIODICITY_MAP = {'each_day': 86400}

def process_add(parser_ns):
    assert parser_ns.source, "No valid source of information provided."
    assert parser_ns.periodicity, "No valid periodicity specified."
    assert parser_ns.filter, "No valid filter for job specified."

    new_filter = NewsFilter(parser_ns.filter)
    new_job = JobMetadata(EXTRACTOR_MAP[parser_ns.source],
                           PERIODICITY_MAP[parser_ns.periodicity],
                           new_filter)
    my_db = Database()
    read_db = my_db.read_from_db(DATABASE_PATH)
    my_db.add_job(new_job)
    my_db.write_local_db_to(DATABASE_PATH)

def process_show():
    my_db = Database()
    my_db.read_from_db(DATABASE_PATH)
    print(my_db)

def process_remove(parser_ns):
    assert isinstance(parser_ns.job_id, int), (
        "Didn't provide a valid id to remove.")

    my_db = Database()
    my_db.read_from_db(DATABASE_PATH)
    my_db.remove_job(parser_ns.job_id)
    my_db.write_local_db_to(DATABASE_PATH)

    print("Removed succesfully")

def start_jobs():
    METADATA_POS = 1
    my_db = Database()
    my_db.read_from_db(DATABASE_PATH)

    for each_entry in my_db:
        # create new job object
        target_metadata = each_entry[METADATA_POS]
        job = ExtractorJob(
            periodicity=target_metadata.periodicity_in_seconds,
            text_filter=target_metadata.words_filter,
            source=target_metadata.target_extractor
        )
        job.test_function()
        job.run()

def create_parser_arguments():
    """Create bash interface."""

    parser = ArgumentParser(description= ('Command line tool to set jobs '
                                          'for oddcrawler daemon.'))
    add_new_job = parser.add_argument_group('Add new Job', (
        'Add a new job to the daemon.'))
    add_new_job.add_argument('-a', '--add', help=('Add a new job to run.'),
                             action='store_true')
    add_new_job.add_argument('--periodicity', choices=PERIODICITY_MAP.keys(),
                             help=(
                                 'Choose how often this script runs. HINT: '
                                 'The default each_day runs at 11:55pm.'))
    add_new_job.add_argument('--source', help=(
        'Specify the news source of the new source.'),
                             choices = EXTRACTOR_MAP.keys())
    add_new_job.add_argument('--filter', type=str, help=(
        'Specify the filters like: (moto+accidente)*fatal. HINT: Use \' \' '
        'around the filter if it contains spaces.'))

    show_job = parser.add_argument_group('Show all jobs')
    show_job.add_argument('-s', '--show', help=('Show all jobs scheduled.'),
                          action='store_true')

    remove_job = parser.add_argument_group('Remove job', (
        'Remove a job from the db using it\'s index'))
    remove_job.add_argument('-r', '--remove', help=('Remove job using id.'),
                            action='store_true')
    remove_job.add_argument('-i', '--job_id', type=int, help=(
        'The job id of the job to remove.'))

    start_jobs = parser.add_argument_group('Start all jobs of database')
    start_jobs.add_argument('--start', action='store_true', help=(
        'Start the daemon, running with the periodicity given, every day '
        'for the day before.'))

    return parser

if __name__ == "__main__":
    parser = create_parser_arguments()
    parser_ns = parser.parse_args()

    print(parser_ns)

    if (parser_ns.add):
        process_add(parser_ns)
    elif (parser_ns.show):
        process_show()
    elif (parser_ns.remove):
        process_remove(parser_ns)
    elif (parser_ns.start):
        print("Start jobs")
        start_jobs()
    else:
        pass
