import sqlite3

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from sqlite_to_postgres.config import dsl
from sqlite_to_postgres.dataclass import (FilmWork, Genre, GenreFilmWork,
                                          Person, PersonFilmWork)
from sqlite_to_postgres.extractor import SQLiteExtractor
from sqlite_to_postgres.saver import PostgresSaver


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection, batch_size: int = 500):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_extractor = SQLiteExtractor(connection)

    data_class_mapping = {
        "film_work": FilmWork,
        "genre": Genre,
        "genre_film_work": GenreFilmWork,
        "person": Person,
        "person_film_work": PersonFilmWork
    }

    for table_name, data_class in data_class_mapping.items():
        for batch in sqlite_extractor.extract_data_as_class(table_name, data_class, batch_size):
            postgres_saver.save_data(batch, table_name)


if __name__ == '__main__':
    with sqlite3.connect('db.sqlite') as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
