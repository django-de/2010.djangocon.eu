import os.path
from fabric.api import *
from fabric.contrib import files

def production():
    env.nickname = 'prod'
    env.hosts = ['thecon@pythonic.nl']
    env.root = '/home/thecon'
    env.venv_root = os.path.join(env.root, 'sites/2011.djangocon.eu/django')
    env.src_root = os.path.join(env.venv_root, 'djangocon')
    env.proj_root = os.path.join(env.src_root, 'djangocon')
    env.pip_file = os.path.join(env.src_root, 'requirements.txt')
    env.manage_py = os.path.join(env.proj_root, 'manage.py')

def update():
   """Update source, update pip requirements, syncdb, restart server"""
   update_proj()
   update_reqs()
   link_settings()
   build_static_files()
   syncdb()

def version():
   """Show last commit to repo on server"""
   require('root', provided_by=[production])
   run('cd %s; git log -1' % env.proj_root)

def update_reqs():
   """Update pip requirements"""
   ve_run('pip install -E %(venv_root)s -r %(pip_file)s' % env)

def update_proj():
   """Updates project source"""
   run('cd %s; git pull origin master' % env.src_root)
   ve_run('cd %s; python setup.py develop'% env.src_root)

def link_settings():
    host_settings = os.path.join(env.proj_root, 'conf', '%s.py' % env.nickname)
    settings = os.path.join(env.proj_root, 'settings.py')
    if files.exists(settings):
        run('rm %s' % settings)
    if files.exists(host_settings):
        run('ln -s %s %s' % (host_settings, settings))
    else:
        print 'No host specific settings file found. Create one at %s' % host_settings

def build_static_files():
    """Runs staticfiles build_static command to collect the various static media files of apps and Django"""
    ve_run('%s build_static --noinput'% env.manage_py)

def syncdb():
   """Run syncdb"""
   ve_run('%s syncdb --noinput' % env.manage_py)
   ve_run('%s migrate' % env.manage_py)

def ve_run(cmd):
   """
   Helper function.
   Runs a command using the virtualenv environment
   """
   require('venv_root')
   return run('source %s/bin/activate; %s' % (env.venv_root, cmd))
