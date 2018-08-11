#!/usr/bin/env python
from hashids import Hashids


class HashIdsClient:

    def __init__(self, salt="somesalt", min_length=6):
        self.hashids = Hashids(salt=salt, min_length=min_length)

    def init_app(self, app):
        self.hashids = Hashids(salt=app['config'].HASH_SALT,
                               min_length=app['config'].HASH_MIN_LENGTH)

    def encode(self, num):
        return self.hashids.encode(num)

    def decode(self, url):
        return self.hashids.decode(url)
