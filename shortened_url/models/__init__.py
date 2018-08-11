#!/usr/bin/env python
from shortened_url.clients import db

# pylint: disable=no-member


class UrlMap(db.Model):

    __tablename__ = 'url_map'

    pid = db.Column(db.BigInteger(), primary_key=True)
    original_url = db.Column(db.Unicode(), nullable=False)
