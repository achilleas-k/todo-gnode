# todo-gnode

Simple web-based todo list.
Uses [Tornado](http://www.tornadoweb.org/) as both a webserver and a web framework.
Items are stored in a [Mongo database](https://github.com/mongodb/mongo).

## Usage

Requires a mongodb service running on the host machine.
If you want to connect to an external Mongo database, edit `dbmanager.py` and set the address and port in the `MongoClient` constructor.

On startup, `tornadoweb.py` reads a file named `cookie_secret`.
This file should contain a secret key which will be used to encrypt the user cookie.

With the database server running and the key set, simply run `tornadoweb.py` to deploy.
By default, the server runs on port `8989`.
The port number can be changed in the `main()` method of `tornadoweb.py`.

The application runs under both Python 2 and Python 3.
Tested with `2.7.10` and `3.5.0`.

## Dependencies

The application depends on the following python libraries:
  - [`tornado`](https://pypi.python.org/pypi/tornado/)
  - [`pymongo`](https://pypi.python.org/pypi/pymongo)
  - [`parsedatetime`](https://pypi.python.org/pypi/parsedatetime/)
