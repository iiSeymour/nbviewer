#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import yaml

class Config(object):

    def __init__(self, conf):
        attrs = set(self.attrs)
        for k, v in conf.items():
            attrs.remove(k)
            setattr(self, k, v)

class WebConfig(Config):
    attrs = frozenset(['port', 'host', 'cookie_secret', 'github_client_id', 'github_client_secret'])

class DBConfig(Config):
    attrs = frozenset(['user', 'database'])

__basename = os.path.dirname(os.path.realpath(__file__))
__conf_file = os.path.join(__basename, 'config.yaml')
__doc = yaml.load(open(__conf_file, 'r'))
web = WebConfig(__doc['web'])
db = DBConfig(__doc['db'])
