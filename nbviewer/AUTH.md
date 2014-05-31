1. Install postgresql

momoko requires psycopg2 

1. In `pg_hba.conf` (usually at `/etc/postgresql/9.3/main/`),
set local access to `trust` (as opposed to the default `peer`)

1. Create an lpmc user/role and database

    sudo psql
    > create user nbviewer;
    > create database nbviewer;
    > grant all privileges on database nbviewer to nbviewer;

1. Restart postgresql

    sudo invoke-rc.d postgresql restart

1. Load the schema

   psql -U nbviewer -d nbviewer < schema.sql

1. Visit [the GitHub applications page](https://github.com/settings/applications)
and register a new developer application.
The authorization callback URL should probably be `http://localhost:5000/auth/github`

1. Copy the `config.yaml.example` to `config.yaml` and edit the configuration
