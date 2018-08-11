#!/usr/bin/env python
import os
import config
import asyncio
import uvloop
from aiohttp import web
from shortened_url import create_app

# Use uvloop :)
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def main():
    loop = asyncio.get_event_loop()
    app = create_app(loop)
    host = os.environ.get('API_HOST', "0.0.0.0")
    port = int(os.environ.get('API_PORT', 5000))
    web.run_app(app, host=host, port=port)


if __name__ == '__main__':
    main()
