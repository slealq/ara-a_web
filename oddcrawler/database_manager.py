"""Manage the jobs database, which contains what the daemon should
execute, and when."""

from oddcrawler import ExtractorJob
from pickle import dump, load, HIGHEST_PROTOCOL
from json import dumps

class Database():
    def __init__(self):
        self._db = {}

    def read_from_db(self, path_to_target):
        """Reads database from file and save it in local."""

        try:
            with open(path_to_target, 'rb') as db_file:
                self._db = load(db_file)
                return self._db
        except FileNotFoundError:
            self._db = {}
            return self._db

    def add_job(self, data: ExtractorJob):
        """Support only single job writes to the database."""

        assert isinstance(data, ExtractorJob), "data should be a ExtractorJob"
        # Use the amount of jobs in db as index
        self._db[len(self._db)] = data

    def remove_job(self, job_id: int):
        """Remove a job id from the db."""

        assert isinstance(job_id, int), "Invalid type of job_id."

        self._db.pop(job_id)

    def write_local_db_to(self, path_to_target: str):
        """Dump local database to file."""

        with open(path_to_target, 'wb') as db_file:
            dump(self._db, db_file, HIGHEST_PROTOCOL)

    def __repr__(self):
        formatted_db = {key: repr(value) for key, value in self._db.items()}

        return dumps(formatted_db, indent=4, sort_keys=True)
