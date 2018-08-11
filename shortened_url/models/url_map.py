#!/usr/bin/env python
from shortened_url.models import UrlMap


async def create_url_map(original_url):
    return await UrlMap.create(original_url=original_url)


async def get_url_map(pid):
    return await UrlMap.get(pid)
