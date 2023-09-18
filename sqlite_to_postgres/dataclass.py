import uuid
from dataclasses import dataclass, field
from datetime import datetime


# Определение структур данных SQLite
@dataclass(frozen=True)
class FilmWork:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    title: str = field(default='')
    description: str = field(default='')
    creation_date: datetime = field(default=datetime.utcnow())
    rating: float = field(default=0.0)
    type: str = field(default='')
    created_at: datetime = field(default=datetime.utcnow())
    updated_at: datetime = field(default=datetime.utcnow())


@dataclass(frozen=True)
class Genre:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    name: str = field(default='')
    description: str = field(default='')
    created_at: datetime = field(default=datetime.utcnow())
    updated_at: datetime = field(default=datetime.utcnow())


@dataclass(frozen=True)
class GenreFilmWork:
    film_work_id: uuid.UUID
    genre_id: uuid.UUID
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime = field(default=datetime.utcnow())


@dataclass(frozen=True)
class Person:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    full_name: str = field(default='')
    created_at: datetime = field(default=datetime.utcnow())
    updated_at: datetime = field(default=datetime.utcnow())


@dataclass(frozen=True)
class PersonFilmWork:
    film_work_id: uuid.UUID
    person_id: uuid.UUID
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    role: str = field(default='')
    created_at: datetime = field(default=datetime.utcnow())
