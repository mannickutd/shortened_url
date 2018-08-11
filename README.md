# shortened_url
Shortened url rest api run on an asychronous web server

# Setting up

* Clone this repository pulling down the submodules as well.
```
git clone git@github.com:DigitalGenius/flow-python-server.git
```

* Create a virtual environment.
```
# NOTE: requires python 3.6+
virtualenv -p python3.6 venv
source venv/bin/activate
```

* Create a local environment.sh file containing the following:
```
echo "
export ENV='DEV'
export SQLALCHEMY_DATABASE_URI="postgresql://localhost/shortened_url"
export SQLALCHEMY_POOL_SIZE='5'
"> environment.sh
```

* Install Postgres [https://www.postgresql.org/download/](https://www.postgresql.org/download/).

* Run the bootstrap script
```
./scripts/bootstrap.sh
```

## Important Libraries

* aiohttp [asynchronous web framework](https://aiohttp.readthedocs.io/en/stable/).
* cython [Python to C compiler](https://github.com/cython/cython).
* uvloop [Ultra fast asyncio event loop](https://github.com/MagicStack/uvloop).
* gino [Python asyncio ORM on SQLAlchemy core](https://github.com/fantix/gino).

## To run the application

To run the aiohttp application
```
scripts/run_api.sh
```

## To run the unit tests

```
scripts/run_tests.sh
```

## Scaling application

* Scaling libraries
The rest api runs on an asynchronous web server aiohttp. Cython is used to help speed up the aiohttp library. Asynchronous web server will scale up the number of http requests to the web server without substantial increases in the amount of memory needed to serve those requests. Asynchronous web server runs on an event loop, we use the uvloop which is a highly optimized event loop built for speed. Having a faster event loop will allow the web server to switch between async events.
The application leverages calls to the db using a superfast binary asynchronous postgres binary protocol (asyncpg). Gino is an extension on top of asyncpg.

* Scaling deployment
The rest api will be run on a linux container. Using linux containers will allow the application to be deployed inside a scalable container orchestration service on the cloud. The container orchestration service will be able to scale the number of containers needed to serve the number of requests to the rest api. An appropriate scaling policy for the rest api service will scale the number of containers as the number of requests changes. Inside the linux container the application is run using gunicorn and nginx as the reverse proxy. Gunicorn gives more control to utilize the resources allocated to each linux container in the container orchestration service and improves fault tolerance running python applications in production.
