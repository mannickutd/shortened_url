#!/usr/bin/env python
import re
from aiohttp import web
from shortened_url.clients import hashids_client
from shortened_url.models.url_map import (get_url_map, create_url_map)

# pylint: disable=unused-argument,invalid-name,broad-except

class InvalidUrlException(Exception):
    def __init__(self, json_msg):
        super(InvalidUrlException, self).__init__()
        self.json_msg = json_msg


URL_REGEX = (r'^(?:http|ftp)s?://' # http:// or https://
             r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain...
             r'localhost|' # localhost...
             r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
             r'(?::\d+)?' # optional port
             r'(?:/?|[/?]\S+)$')

REGEX = re.compile(URL_REGEX, re.IGNORECASE)


def _validate_url(url):
    # There is several ways to approach this.
    # Depending on the users of the system the validation would be adapted for who is using the
    # the system.
    # First approach would be to use the regex approach.
    # I have gone with a tried and tested regex approach from django described on the stackoverflow
    # url https://stackoverflow.com/questions/7160737/python-how-to-validate-a-url-in-python-malformed-or-not
    match = re.match(REGEX, url)
    if not match:
        # The above regex doesn't match with the pattern that excludes the example
        # given in the requirement www.example.com.
        # We could prepend http:// to the beginning of the url or in the future look
        # to exclude the clause from the regex expression
        match = re.match(REGEX, 'http://{0}'.format(url))
        if not match:
            # More work could be done here using urllib.parse.urlparse to give users
            # specific errors how the url is invalid.
            # I would possibly avoid this unless there is a specific requirement.
            # Testing would need to be done on how slow using urllib.parse.urlparse is.
            raise InvalidUrlException({
                'url': 'Invalid url passed should conform to the regex {0}'.format(URL_REGEX)})
    # Another approach would be to actually test the url provided and validate the response.
    # This approach would also need error handling on why the url is invalid.


async def url_map_post(request):
    try:
        data = await request.json()
        url = data['url']
    except Exception as e:
        return web.json_response({'status': 'error',
                                  'message': {'url': "invalid or missing parameter"}})
    try:
        _validate_url(url)
    except InvalidUrlException as e:
        return web.json_response({'status': 'error',
                                  'message': e.json_msg})
    url_map = await create_url_map(url)
    relative_url = request.app.router['url_map_get'].url_for(
        short_url=hashids_client.encode(url_map.pid))
    return web.json_response({
        'shortened_url': str(request.url.join(relative_url))})


async def url_map_get(request):
    url_map_pid = hashids_client.decode(request.match_info.get('short_url'))[0]
    url_map = await get_url_map(url_map_pid)
    if not url_map:
        raise web.HTTPNotFound()
    raise web.HTTPFound(url_map.original_url)
