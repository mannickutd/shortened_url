#!/usr/bin/env python
import logging
from aiohttp import (web, client_exceptions)
import sqlalchemy as sa
from shortened_url.clients import (db, hashids_client)
from config import Config

# pylint: disable=invalid-name,unused-variable,unused-argument,broad-except

logger = logging.getLogger('aiohttp.server')


async def init_gino(app):
    from shortened_url.models import (UrlMap)
    # Replace synchronous db engine with asynchronous gino.
    engine = await db.set_bind(app['config'].SQLALCHEMY_DATABASE_URI,
                               min_size=1,
                               max_size=app['config'].SQLALCHEMY_POOL_SIZE)


async def close_gino(app):
    await db.pop_bind().close()


def _init_db(app):
    app.on_startup.append(init_gino)
    app.on_cleanup.append(close_gino)
    # Create tables synchronously
    db_engine = sa.create_engine(app['config'].SQLALCHEMY_DATABASE_URI,
                                 pool_size=app['config'].SQLALCHEMY_POOL_SIZE)
    db.create_all(bind=db_engine)


def _add_handlers(app):
    from shortened_url.url_map_rest import (url_map_get, url_map_post)
    app.router.add_get('/{short_url}', url_map_get, name="url_map_get")
    app.router.add_post('/', url_map_post, name="url_map_post")


@web.middleware
async def error_json_middleware(request, handler):
    try:
        response = await handler(request)
        return response
    except web.HTTPFound as ex:
        # Ignore redirects
        raise ex
    except web.HTTPException as ex:
        # pylint: disable=no-member
        return web.json_response({"message": ex.json_body if hasattr(ex, 'json_body') else ex.text}, status=ex.status)
    except Exception:
        logger.error("Unknown exception", exc_info=True)
        return web.json_response({"message": "Unknown error"}, status=500)


def create_app(loop):
    # Set logger level
    log_level = logging.DEBUG if Config.ENV != 'prod' else logging.ERROR
    logger.setLevel(log_level)
    app = web.Application(loop=loop, middlewares=[error_json_middleware], client_max_size=50000000)
    app['config'] = Config
    _init_db(app)
    hashids_client.init_app(app)
    # To be done
    _add_handlers(app)
    # Set SA engine level
    logging.getLogger('sqlalchemy.engine').setLevel(log_level)
    logging.getLogger('gino.engine._SAEngine').setLevel(log_level)
    return app
