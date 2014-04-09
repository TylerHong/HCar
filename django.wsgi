import os
import sys

sys.path.append('/home/kshong/PROJECT/hcar')
os.environ['DJANGO_SETTINGS_MODULE'] = 'hcar.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
