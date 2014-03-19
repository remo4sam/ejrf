#!/bin/bash

cd ..
source ejrf_env/bin/activate
cd ejrf
cp eJRF/snap-ci/snap-settings.py eJRF/localsettings.py
coverage run manage.py test