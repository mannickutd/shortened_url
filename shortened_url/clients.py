#!/usr/bin/env python
from gino import Gino
from shortened_url.hashids_client import HashIdsClient

# pylint: disable=invalid-name

db = Gino()
hashids_client = HashIdsClient()
