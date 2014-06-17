"""
WSGI config for Editores project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""

import os

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from django.http import absolute_http_url_re, urljoin, iri_to_uri

# Apply WSGI middleware here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)


def build_absolute_uri(self, location=None):
    """
    Builds an absolute URI from the location and the variables available in
    this request. If no location is specified, the absolute URI is built on
    ``request.get_full_path()``.
    """
    if not location:
        location = self.get_full_path()
    if not absolute_http_url_re.match(location):
        current_uri = '%s://%s%s' % (self.is_secure() and 'https' or 'http',
                                     self.get_host(), self.path)
        location = urljoin(current_uri, location)
    return iri_to_uri(location)

def is_secure(self):
    return os.environ.get("HTTPS") == "on"
