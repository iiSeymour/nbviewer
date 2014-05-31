#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import hashlib
import tornado.gen
import tornado.auth
import tornado.escape
import nbviewer.config
import tornado.httputil
import tornado.httpclient


from tornado.log import app_log, access_log


class GithubMixin(tornado.auth.OAuth2Mixin):

    _OAUTH_AUTHORIZE_URL = 'https://github.com/login/oauth/authorize'
    _OAUTH_ACCESS_TOKEN_URL = 'https://github.com/login/oauth/access_token'

    def authorize_redirect(self, **kwargs):
        kwargs['client_id'] = nbviewer.config.web.github_client_id
        super(GithubMixin, self).authorize_redirect(**kwargs)

    @tornado.gen.coroutine
    def get_authenticated_user(self, redirect_uri, code):
        url = self._oauth_request_token_url(redirect_uri=redirect_uri, code=code,
                                            client_id=nbviewer.config.web.github_client_id,
                                            client_secret=nbviewer.config.web.github_client_secret)
        response = yield self._http(url)
        data = tornado.escape.json_decode(response.body)
        access_token = data['access_token']

        user = yield self.github_request('/user', access_token)
        user['access_token'] = access_token
        raise tornado.gen.Return(user)

    @tornado.gen.coroutine
    def github_request(self, path, access_token=None, method='GET', headers={}, body=None, **args):
        args['access_token'] = access_token
        url = tornado.httputil.url_concat('https://api.github.com' + path, args)
        if body is not None:
            body = tornado.escape.json_encode(body)
        response = yield self._http(url, method=method, headers=headers, body=body)
        raise tornado.gen.Return(tornado.escape.json_decode(response.body))

    @staticmethod
    @tornado.gen.coroutine
    def _http(*args, **kwargs):
        headers = {'Accept': 'application/json', 'User-Agent': 'nbviewer'}
        headers.update(kwargs.get('headers', {}))
        kwargs['headers'] = headers
        response = yield tornado.httpclient.AsyncHTTPClient().fetch(*args, **kwargs)
        if response.error:
            raise Exception('%s\n%s' % (response.error, response.body))
        raise tornado.gen.Return(response)

    @staticmethod
    def avatar_url(username, email):
        default = 'https://identicons.github.com/%s.png' % username
        if not email:
            return default
        md5 = hashlib.md5(email.encode('utf-8'))
        return 'http://www.gravatar.com/avatar/%s?s=20&d=%s' % (md5.hexdigest(), urllib.quote(default))
