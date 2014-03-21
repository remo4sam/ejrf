#!/bin/bash

cd ..
virtualenv ejrf_env
source ejrf_env/bin/activate
cd ejrf
pip install -r eJRF/GO/pip-requirements.txt
pip install coveralls
cp eJRF/GO/go-settings.py eJRF/localsettings.py
psql -h localhost -U ejrf -c 'drop database ejrf_test'
psql -h localhost -U ejrf -c 'create database ejrf_test'
./manage.py syncdb --noinput
./manage.py migrate