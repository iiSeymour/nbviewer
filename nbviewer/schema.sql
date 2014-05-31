DROP TABLE IF EXISTS contact_info;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    github_id integer PRIMARY KEY,
    username varchar(32) NOT NULL UNIQUE,
    access_token varchar NOT NULL UNIQUE
);

CREATE TABLE contact_info (
    github_id integer NOT NULL references users(github_id),
    email varchar(64) NOT NULL,
    constraint contact_info_unique unique(github_id)
);
