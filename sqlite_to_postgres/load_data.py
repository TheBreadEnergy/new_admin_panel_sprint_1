import sqlite3
from typing import List

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from sqlite_to_postgres.dataclass import (FilmWork, Genre, GenreFilmWork,
                                          Person, PersonFilmWork)
from sqlite_to_postgres.saver import PostgresSaver
from sqlite_to_postgres.extractor import SQLiteExtractor


def batch_data(data: List, batch_size: int) -> List[List]:
    """Делит данные на пакеты заданного размера."""
    return [data[i:i + batch_size] for i in range(0, len(data), batch_size)]


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
        data = sqlite_extractor.extract_data_as_class(table_name, data_class)
        for batch in batch_data(data, batch_size):
            postgres_saver.save_data(batch, table_name)


if __name__ == '__main__':
    dsl = {'dbname': 'movies_database', 'user': 'app', 'password': '123qwe', 'host': '127.0.0.1', 'port': 5432}
    with sqlite3.connect('db.sqlite') as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
