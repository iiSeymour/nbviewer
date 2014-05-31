#!/usr/bin/env python
# -*- coding: utf-8 -*-

import momoko
import psycopg2
import tornado.gen
from nbviewer.config import db


class MomokoDB(object):

    db = momoko.Pool(dsn='dbname=%s user=%s' % (db.database, db.user), size=2)

    @tornado.gen.coroutine
    def execute(self, query, *args):
        result = yield momoko.Op(self.db.execute, query, args, cursor_factory=psycopg2.extras.DictCursor)
        raise tornado.gen.Return(result)

    @tornado.gen.coroutine
    def create_user(self, user):
        query = 'INSERT INTO users (github_id, username, access_token) VALUES (%s, %s, %s);'
        yield self.execute(query, user['id'], user['login'], user['access_token'])

    @tornado.gen.coroutine
    def update_access_token(self, user):
        query = 'UPDATE users SET access_token = %s WHERE github_id = %s;'
        cursor = yield self.execute(query, user['access_token'], user['id'])
        raise tornado.gen.Return(cursor.rowcount)

    @tornado.gen.coroutine
    def set_contact_info(self, github_id, email):
        try:
            query = 'INSERT INTO contact_info (github_id, email) VALUES(%s, %s);'
            yield self.execute(query, github_id, email)
        except psycopg2.IntegrityError:
            query = 'UPDATE contact_info SET email = %s WHERE github_id = %s;'
            yield self.execute(query, email, github_id)

    @tornado.gen.coroutine
    def get_user(self, github_id):
        query = 'SELECT github_id, username, access_token FROM users WHERE github_id = %s;'
        cursor = yield self.execute(query, github_id)
        raise tornado.gen.Return(cursor.fetchone())

    @tornado.gen.coroutine
    def get_user_by(self, field, value):
        query = 'SELECT github_id, username, access_token FROM users WHERE ' + field + ' = %s;'
        cursor = yield self.execute(query, value)
        raise tornado.gen.Return(cursor.fetchone())

    @tornado.gen.coroutine
    def get_contact_info(self, github_id):
        query = 'SELECT email FROM contact_info WHERE github_id = %s;'
        cursor = yield self.execute(query, github_id)
        raise tornado.gen.Return(cursor.fetchone()[0])

    @tornado.gen.coroutine
    def get_user_ids(self):
        query = 'SELECT users.github_id FROM users'
        cursor = yield self.execute(query)
        raise tornado.gen.Return(cursor.fetchall())

    @tornado.gen.coroutine
    def delete_user(self, github_id):
        query = 'DELETE FROM contact_info WHERE github_id = %s;'
        yield self.execute(query, github_id)
        query = 'DELETE FROM users WHERE github_id = %s;'
        yield self.execute(query, github_id)
