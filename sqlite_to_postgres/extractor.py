import dataclasses
import sqlite3
from typing import Any, Generator, List, Type


class SQLiteExtractor:
    """Класс для извлечения данных из SQLite."""

    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection

    def extract_data_as_class(self, table_name: str, data_class: Type, batch_size: int = 1000) -> (
            Generator)[List[Any], None, None]:
        """Извлекает данные из SQLite и возвращает их как список экземпляров dataclass."""
        cursor = self.connection.cursor()
        columns = [i.name for i in dataclasses.fields(data_class)]
        sqlite_columns = ", ".join(columns)
        cursor.execute(f"SELECT {sqlite_columns} FROM {table_name}")

        # Получение значений по умолчанию из dataclass
        default_values = {f.name: f.default for f in dataclasses.fields(data_class) if
                          f.default is not dataclasses.MISSING}

        while True:
            rows = cursor.fetchmany(batch_size)
            if not rows:
                break

            result = []
            for row in rows:
                row_dict = {f.name: None for f in dataclasses.fields(data_class)}
                fetched_data = dict(zip(columns, row))

                for key in row_dict.keys():
                    if key in fetched_data and fetched_data[key] is not None:
                        row_dict[key] = fetched_data[key]
                    elif key in default_values:
                        row_dict[key] = default_values[key]() if callable(default_values[key]) else default_values[key]

                result.append(data_class(**row_dict))

            yield result

        cursor.close()
