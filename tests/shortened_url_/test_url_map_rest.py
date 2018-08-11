#!/usr/bin/env python
import json
import pytest
from shortened_url.url_map_rest import (_validate_url, InvalidUrlException)


async def test_url_map_get(async_app, sample_short_url, sample_url_map):
    test_client = async_app[0]
    resp = await test_client.get('/{0}'.format(sample_short_url), allow_redirects=False)
    assert resp.status == 302
    assert resp.headers['Location'] == sample_url_map.original_url


async def test_url_map_get_404(async_app, sample_short_url):
    test_client = async_app[0]
    resp = await test_client.get('/{0}'.format(sample_short_url))
    assert resp.status == 404


async def test_url_map_post(async_app, db_, sample_original_url):
    test_client = async_app[0]
    resp = await test_client.post('/',
                                  data=json.dumps({'url': sample_original_url}))
    json_resp = await resp.json()
    assert json_resp['shortened_url']


async def test_url_map_post_missing_json(async_app):
    test_client = async_app[0]
    resp = await test_client.post('/', data=json.dumps({'blah': ''}))
    json_resp = await resp.json()
    assert json_resp['status'] == 'error'
    assert 'invalid or missing parameter' in json_resp['message']['url']


async def test_url_map_post_invalid_url(async_app):
    test_client = async_app[0]
    resp = await test_client.post('/', data=json.dumps({'url': 'blah'}))
    json_resp = await resp.json()
    assert json_resp['status'] == 'error'
    assert 'Invalid url passed should conform to the regex' in json_resp['message']['url']


@pytest.mark.parametrize("test_url,is_success", [
    # Small sample size of valid urls that could be tested.
    # Success
    ("www.google.com", True),
    ("http://www.google.com", True),
    ("https://www.google.com", True),
    ("http://google.com", True),
    ('http://www.google', True),
    # Errors
    (".ww.google.com", False),
    ("*google.com", False),
    ("www..google.com", False),
    ("www.google..", False),
    ("htp://www.google.com", False)
])
def test_validate_url(test_url, is_success):
    if is_success:
        _validate_url(test_url)
    else:
        with pytest.raises(InvalidUrlException) as e:
            _validate_url(test_url)
