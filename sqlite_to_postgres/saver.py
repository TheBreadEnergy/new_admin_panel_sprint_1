from typing import Any, List

import psycopg2
from psycopg2.extensions import connection as _connection

from config import logger


class PostgresSaver:
    """Класс для сохранения данных в PostgreSQL."""

    def __init__(self, connection: _connection):
        self.connection = connection
        # Соответствие столбцов SQLite к PostgreSQL
        self.column_mapping = {
            "created_at": "created",
            "updated_at": "modified"
        }

    def save_data(self, data: List[Any], table_name: str):
        """Сохраняет список экземпляров dataclass в PostgreSQL."""
        cursor = self.connection.cursor()

        columns = data[0].__annotations__.keys()
        columns_str = ", ".join(columns)
        for orig, repl in self.column_mapping.items():
            columns_str = columns_str.replace(orig, repl)
        col_count = ', '.join(['%s'] * len(columns))

        values = [tuple(item.__dict__.values()) for item in data]
        bind_values = ','.join(cursor.mogrify(f"({col_count})", value).decode('utf-8') for value in values)

        query = (f'INSERT INTO content.{table_name} ({columns_str}) VALUES {bind_values} '
                 f'ON CONFLICT (id) DO NOTHING')
        try:
            cursor.execute(query)
        except psycopg2.Error as e:
            logger.error(f"Ошибка при вставке в {table_name}. Ошибка: {e}")
        self.connection.commit()
        cursor.close()
