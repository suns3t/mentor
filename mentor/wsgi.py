"""
WSGI config for mentor project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
import site
import sys

# add the virtualenv
root = os.path.normpath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.append(root)
site.addsitedir(os.path.join(root, ".env/lib/python2.6/site-packages"))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mentor.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
