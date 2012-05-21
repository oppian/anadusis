anadusis
========

A django based social networking site using pinax.

It has a custom app that handles video transcoding and supports display using an Adobe Flash-based video player.


Dependencies
------------

This project makes use of [virtualenv](http://pypi.python.org/pypi/virtualenv)

Setup
-----

To setup development environment:

```bash
/System/Library/Frameworks/Python.framework/Versions/2.6/Resources/Python.app/Contents/MacOS/Python  lib/pinax/scripts/pinax-boot.py --development --source=lib/pinax pinax-env

source pinax-env/bin/activate
```

To install rquirements:

```bash
pip install --no-deps --requirement requirements.txt
```

To synchronise the database:
```bash
python manage.py syncdb
python manage.py migrate
```

To run a local server:
```bash
python manage.py runserver_plus 0.0.0.0:8080
```