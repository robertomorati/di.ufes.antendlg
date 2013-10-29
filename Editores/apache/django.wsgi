import os
import sys

sys.path.append('/home/di.ufes.antendlg/Editores')
sys.path.append('/home/di.ufes.antendlg/Editores/editores')
os.environ['DJANGO_SETTINGS_MODULE'] = 'editores.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()