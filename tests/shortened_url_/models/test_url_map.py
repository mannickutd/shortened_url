#!/usr/bin/env python
from shortened_url import db
from shortened_url.models.url_map import (UrlMap, create_url_map, get_url_map)


async def test_create_url_map(db_, sample_original_url):
    assert len(await db.all(UrlMap.query)) == 0
    url_map = await create_url_map(sample_original_url)
    assert len(await db.all(UrlMap.query)) == 1
    first = await db.first(UrlMap.query)
    assert first.original_url == sample_original_url    


async def get_url_map(db_, sample_url_map):
    assert len(await db.all(UrlMap.query)) == 1
    url_map = await get_url_map(sample_url_map)
    assert url_map.original_url == sample_url_map.original_url
