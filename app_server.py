#!/usr/bin/env python
import config
import asyncio
import uvloop
from shortened_url import create_app

loop = asyncio.get_event_loop()
app = create_app(loop)
