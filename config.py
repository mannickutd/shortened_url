#!/usr/bin/env python
import os


class Config:
    ENV = os.environ['ENV']
    SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']
    SQLALCHEMY_POOL_SIZE = int(os.environ['SQLALCHEMY_POOL_SIZE'])

    HASH_MIN_LENGTH = 8
    HASH_SALT = "SomeLittleSecret"

    