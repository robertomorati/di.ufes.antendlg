#!/usr/bin/python
import os, site, sys

# virtualenv bug
os.environ['PATH'] = os.path.dirname(__file__)

# active virtualenv
venv = os.path.join(os.path.dirname(__file__), '../env/bin/activate_this.py')
execfile(venv, dict(__file__=venv))

# default path
path = os.path.join(os.path.dirname(__file__), '../')
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "robertomorati.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

