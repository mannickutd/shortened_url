#!/usr/bin/env python

import os

import pytest
import sqlalchemy as sa
from shortened_url import create_app
from shortened_url.clients import (db, hashids_client)
from shortened_url.models import UrlMap


@pytest.fixture
def async_app(test_client, loop):
    app = create_app(loop)
    return loop.run_until_complete(test_client(app)), app


@pytest.fixture
def db_(request, loop, async_app):
    def teardown():
        app_ = async_app[1]
        db_engine = sa.create_engine(app_['config'].SQLALCHEMY_DATABASE_URI)
        for table in reversed(db.sorted_tables):
            db_engine.execute(table.delete())

    request.addfinalizer(teardown)
    return db


@pytest.fixture(scope='session')
def sample_original_url():
    return "http://www.google.com"


@pytest.fixture(scope='session')
def sample_number():
    return 1000


@pytest.fixture
async def sample_url_map(db_, sample_number, sample_original_url):
    return await UrlMap.create(pid=sample_number, original_url=sample_original_url)


@pytest.fixture
def sample_short_url(sample_number):
    return hashids_client.encode(sample_number)
