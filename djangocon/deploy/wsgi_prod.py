import os
import sys 
import site 

# redirect sys.stdout to sys.stderr for bad libraries like geopy that uses
# print statements for optional import exceptions.
sys.stdout = sys.stderr

# Remember original sys.path.
prev_sys_path = list(sys.path) 

ALLDIRS = ['/home/djangocon/lib/python2.5/site-packages']

# Add each new site-packages directory.
for directory in ALLDIRS:
  site.addsitedir(directory)

# Reorder sys.path so new directories at the front.
new_sys_path = [] 
for item in list(sys.path): 
    if item not in prev_sys_path: 
        new_sys_path.append(item) 
        sys.path.remove(item) 
sys.path[:0] = new_sys_path

from django.conf import settings
os.environ["DJANGO_SETTINGS_MODULE"] = "djangocon.conf.prod"

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()
