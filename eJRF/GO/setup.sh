#!/bin/bash

cd ..
virtualenv ejrf_env
source ejrf_env/bin/activate
cd ejrf
pip install -r eJRF/GO/pip-requirements.txt
pip install coveralls
cp eJRF/GO/go-settings.py eJRF/localsettings.py
./manage.py syncdb --noinput
./manage.py migrate