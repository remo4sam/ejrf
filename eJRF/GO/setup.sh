#!/bin/sh
pip install -r pip-requirements.txt
pip install coveralls
copy eJRF/GO/go-settings.py eJRF/localsettings.py
./manage.py syncdb --noinput
./manage.py migrate