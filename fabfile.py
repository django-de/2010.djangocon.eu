from os.path import join
from fabric.api import *
from fabric.contrib import files

env.hosts = ['djangocon@phaia.rdev.info']
env.root = '/home/djangocon'
env.src_root = join(env.root, 'src/djangocon')
env.proj_root = join(env.src_root, 'djangocon')
env.pip_file = join(env.src_root, 'requirements.txt')

def update():
   """Update source, update pip requirements, syncdb, restart server"""
   update_proj()
   update_reqs()
   link_settings()
   syncdb()
   restart()

def version():
   """Show last commit to repo on server"""
   run('cd %s; git log -1' % env.proj_root)

def restart():
   """Restart Apache process"""
   run('touch %s' % join(env.src_root, 'deploy/djangocon.wsgi'))

def update_reqs():
   """Update pip requirements"""
   ve_run('pip install -E %s -r %s' % (env.root, env.pip_file))

def update_proj():
   """Updates project source"""
   run('cd %s; git pull origin master' % env.src_root)
   ve_run('cd %s; python setup.py develop'% env.src_root)

def link_settings():
    host_settings = join(env.proj_root, 'conf', '%s.py' % env.get('host'))
    settings = join(env.proj_root, 'settings.py')
    if files.exists(settings):
        run('rm %s' % settings)
    if files.exists(host_settings):
        run('ln -s %s %s' % (host_settings, settings))
    else:
        print 'No host specific settings file found. Create one at %s' % host_settings

def syncdb():
   """Run syncdb"""
   output = ve_run('%s syncdb' % join(env.proj_root, 'manage.py'))

def ve_run(cmd):
   """
   Helper function.
   Runs a command using the virtualenv environment
   """
   require('root')
   return run('source %s/bin/activate; %s' % (env.root, cmd))
