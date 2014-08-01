import os
import sys

sys.path.append('/var/www/dev.autenvldg/Editores')
sys.path.append('/var/www/dev.autenvldg/Editores/editores')
os.environ['DJANGO_SETTINGS_MODULE'] = 'editores.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()