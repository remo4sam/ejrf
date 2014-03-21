#!/bin/bash

cd ..
source ejrf_env/bin/activate
cd ejrf
cp eJRF/GO/go-settings.py eJRF/localsettings.py
cp eJRF/GO/go_steps.py questionnaire/features/initial_steps.py
./manage.py harvest