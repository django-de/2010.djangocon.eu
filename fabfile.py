from os.path import join
from fabric.api import *
from fabric.contrib import files

env.hosts = ['djangocon@phaia.rdev.info']
env.root = '/home/djangocon'
env.src_root = join(env.root, 'src/djangocon')
env.proj_root = join(env.src_root, 'djangocon')
env.pip_file = join(env.src_root, 'requirements.txt')
env.pid_file = '/tmp/djangocon.pid'
env.deploy_dir = join(env.proj_root, 'deploy')
env.gunicorn_config = join(env.deploy_dir, 'gunicorn.conf.py')
env.nginx_config = join(env.deploy_dir, 'nginx.conf')

def update():
   """Update source, update pip requirements, syncdb, restart server"""
   update_proj()
   update_reqs()
   link_settings()
   copy_nginx_config()
   syncdb()
   restart_gunicorn()

def version():
   """Show last commit to repo on server"""
   run('cd %s; git log -1' % env.proj_root)

def restart_gunicorn():
    """Restart gunicorn process"""
    if not files.exists(env.pid_file):
        return
    pid = run('cat %s' % env.pid_file).strip()
    if pid:
        run('kill -HUP %s' % pid)
    else:
        print "No PID file at %s found." % env.pid_file

def restart_nginx():
    """Restart Nginx process"""
    sudo('/etc/init.d/nginx restart')

def update_reqs():
   """Update pip requirements"""
   ve_run('pip install -E %(root)s -r %(pip_file)s' % env)

def update_proj():
   """Updates project source"""
   run('cd %s; git pull origin master' % env.src_root)
   ve_run('cd %s; python setup.py develop'% env.src_root)

def link_settings():
    host_settings = join(env.proj_root, 'conf', '%s.py' % env.host)
    settings = join(env.proj_root, 'settings.py')
    if files.exists(settings):
        run('rm %s' % settings)
    if files.exists(host_settings):
        run('ln -s %s %s' % (host_settings, settings))
    else:
        print 'No host specific settings file found. Create one at %s' % host_settings

def copy_nginx_config():
    sudo('cp %(nginx_config)s /etc/nginx/conf.d/djangocon.conf' % env)

def start_gunicorn():
    require('update_reqs')
    run('gunicorn djangocon.deploy.wsgi --config %(gunicorn_config)s -w 4 -p %(pid_file)s --daemon' % env)

def syncdb():
   """Run syncdb"""
   manage_py = join(env.proj_root, 'manage.py')
   ve_run('%s syncdb --noinput' % manage_py)
   ve_run('%s migrate' % manage_py)

def ve_run(cmd):
   """
   Helper function.
   Runs a command using the virtualenv environment
   """
   require('root')
   return run('source %s/bin/activate; %s' % (env.root, cmd))
