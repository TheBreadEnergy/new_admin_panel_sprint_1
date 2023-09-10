CREATE SCHEMA content;

CREATE TABLE IF NOT EXISTS content.film_work
(
    id            uuid PRIMARY KEY,
    title         TEXT NOT NULL,
    description   TEXT,
    creation_date DATE,
    rating        FLOAT,
    type          TEXT not null,
    created       timestamp with time zone,
    modified      timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.genre
(
    id          uuid PRIMARY KEY,
    name        TEXT not null,
    description TEXT,
    created_at  timestamp with time zone,
    updated_at  timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.genre_film_work
(
    id           uuid PRIMARY KEY,
    film_work_id TEXT not null,
    genre_id     TEXT not null,
    created_at   timestamp with time zone
);

CREATE UNIQUE INDEX film_work_genre
    ON content.genre_film_work (film_work_id, genre_id);

CREATE TABLE IF NOT EXISTS content.person
(
    id         uuid PRIMARY KEY,
    full_name  text not null,
    created_at timestamp with time zone,
    updated_at timestamp with time zone
);


CREATE TABLE IF NOT EXISTS content.person
(
    id         uuid PRIMARY KEY,
    full_name  text not null,
    created_at timestamp with time zone,
    updated_at timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.person_film_work
(
    id           uuid PRIMARY KEY,
    film_work_id TEXT not null,
    person_id    TEXT not null,
    role         TEXT not null,
    created_at   timestamp with time zone
);

create unique index film_work_person_role
    on content.person_film_work (film_work_id, person_id, role);