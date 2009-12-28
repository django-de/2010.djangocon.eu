from os.path import join
from fabric.api import *

env.hosts = ['eurodjangocon@djangocon.eu']
env.root = '/home/eurodjangocon'
env.proj_root = join(env.root, 'src/djangocon')
env.pip_file = join(env.proj_root, 'djangocon/requirements.txt')

def update():
   """Update source, update pip requirements, syncdb, restart server"""
   update_proj()
   update_reqs()
   syncdb()
   restart()

def version():
   """Show last commit to repo on server"""
   run('cd %s; hg log -l 1' % env.proj_root)

def restart():
   """Restart Apache process"""
   run('touch %s' % join(env.proj_root, 'deploy/djangocon.wsgi'))

def update_reqs():
   """Update pip requirements"""
   ve_run('pip install -E %s -r %s' % (env.root, env.pip_file))

def update_proj():
   """Updates project source"""
   run('cd %s; hg pull --update' % env.proj_root)
   ve_run('cd %s; python setup.py develop'% env.proj_root)

def syncdb():
   """Run syncdb"""
   output = ve_run('%s syncdb' % join(env.proj_root, 'djangocon/manage.py'))

def ve_run(cmd):
   """
   Helper function.
   Runs a command using the virtualenv environment
   """
   require('root')
   return run('source %s/bin/activate; %s' % (env.root, cmd))
