#!/usr/bin/env python
from shortened_url.clients import hashids_client


def test_hashids_client_encode(async_app, sample_number):
    short_url = hashids_client.encode(sample_number)
    assert len(short_url) >= async_app[1]['config'].HASH_MIN_LENGTH


def test_hashids_client_decode(sample_number):
    short_url = hashids_client.encode(sample_number)
    assert sample_number == hashids_client.decode(short_url)[0]
