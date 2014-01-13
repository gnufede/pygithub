Free implementantion of a Github-like site in Flask.
====================================================

Steps to get it working
-----------------------

Create and activate a virtualenv:

    $ virtualenv --distribute -p /usr/bin/python-2.7 pygithub_env
    $ . pygithub_env/bin/activate

Install the requirements:

    $ pip install -r requirements.txt

Run:

    $ cd pygithub
    $ python main.py


Notes
-----

At the moment only accepts pushing/pulling from repositories via SSH. The suggested remote command can be wrong if you have SSH running on a different port.


Python 3
--------

Not compatible yet due to git-python

