# todo-gnode

Simple web-based todo list.
Uses [Tornado](http://www.tornadoweb.org/) as both a webserver and a web framework.
Items are stored in a [Mongo database](https://github.com/mongodb/mongo).

## Usage

This requires a mongodb service running on the host machine.
If you want to connect to an external Mongo database, edit `dbmanager.py` and set the address and port in the `MongoClient` constructor.

On startup, `tornadoweb.py` reads a file named `cookie_secret`.
This should contain a secret key which will be used to encrypt the user cookie.

With the database server running and the key set, simply run `tornadoweb.py` to deploy.
By default, the server runs on port `8989`. This can be changed in the `main()` method of `tornadoweb.py`.
