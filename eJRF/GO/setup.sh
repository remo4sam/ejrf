pip install -r pip-requirements.txt
pip install coveralls
cp eJRF/GO/go-settings.py eJRF/localsettings.py
./manage.py syncdb --noinput
./manage.py migrate