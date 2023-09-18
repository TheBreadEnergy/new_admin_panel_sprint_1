import sqlite3
import psycopg2
import os
from datetime import datetime


def get_sqlite_count(connection, table_name):
    cursor = connection.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    return cursor.fetchone()[0]


def get_pg_count(connection, table_name):
    cursor = connection.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM content.{table_name}")
    return cursor.fetchone()[0]


def compare_counts(sqlite_count, pg_count, table_name):
    assert sqlite_count == pg_count, (f"Counts do not match for table {table_name}:"
                                      f" SQLite has {sqlite_count} rows, PostgreSQL has {pg_count} rows.")


def extract_column_names(connection, table_name):
    cursor = connection.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    return [column[1] for column in columns]


def extract_pg_column_names(connection, table_name, schema='content'):
    cursor = connection.cursor()
    query = (f"SELECT column_name "
             f"FROM information_schema.columns "
             f"WHERE table_schema = '{schema}' AND table_name = '{table_name}';")
    cursor.execute(query)
    columns = cursor.fetchall()
    return [column[0] for column in columns]


def get_sqlite_data(connection, table_name):
    columns = extract_column_names(connection, table_name)
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    return [dict(zip(columns, row)) for row in rows]


def get_pg_data(connection, table_name, schema='content'):
    columns = extract_pg_column_names(connection, table_name, schema)
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {schema}.{table_name}")
    rows = cursor.fetchall()

    return [dict(zip(columns, row)) for row in rows]


def map_sqlite_row_to_pg_format(sqlite_row, column_mapping):
    mapped_row = {}
    for key, value in sqlite_row.items():
        if key in column_mapping:
            mapped_row[column_mapping[key]] = value
        else:
            mapped_row[key] = value

    return mapped_row


def rows_are_equivalent(row1, row2):
    for key, value in row1.items():
        if value is None and key in row2:
            continue
        if key == 'file_path':
            continue
        if key not in row2:
            return False

        # Если row2[key] является datetime и value - строкой
        if isinstance(row2[key], datetime) and isinstance(value, str):
            try:
                if value.endswith('+00'):
                    value = value[:-2] + '00:00'

                dt_value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S.%f%z')
                if dt_value != row2[key]:
                    return False
            except ValueError:
                return False
        elif str(row2[key]) != str(value):
            return False

    return True


def compare_rows(sqlite_data, pg_data, table_name):
    column_mapping = {
        "created_at": "created",
        "updated_at": "modified"
    }
    for i in range(len(sqlite_data)):
        mapped_row = map_sqlite_row_to_pg_format(sqlite_data[i], column_mapping)

        # Поиск соответствующей строки в pg_data
        equivalent_row_exists = rows_are_equivalent(mapped_row, pg_data[i])

        assert equivalent_row_exists, f"Row {sqlite_data[i]} from table {table_name}."


def test_data_integrity():
    base_directory = os.getcwd().split("sqlite_to_postgres")[0] + "sqlite_to_postgres"
    path_to_sqlite = os.path.join(base_directory, 'db.sqlite')
    sqlite_conn = sqlite3.connect(path_to_sqlite)
    dsl = {'dbname': 'movies_database', 'user': 'app', 'password': '123qwe', 'host': '127.0.0.1', 'port': 5432}
    pg_conn = psycopg2.connect(**dsl)

    tables = ["genre", "film_work", "person", "genre_film_work", "person_film_work"]
    for table_name in tables:
        sqlite_count = get_sqlite_count(sqlite_conn, table_name)
        pg_count = get_pg_count(pg_conn, table_name)

        compare_counts(sqlite_count, pg_count, table_name)

        sqlite_data = get_sqlite_data(sqlite_conn, table_name)
        pg_data = get_pg_data(pg_conn, table_name)

        compare_rows(sqlite_data, pg_data, table_name)

    sqlite_conn.close()
    pg_conn.close()
