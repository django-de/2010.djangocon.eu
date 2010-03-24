from os.path import join
from fabric.api import *
from fabric.contrib import files

def production():
    env.hosts = ['djangocon@phaia.rdev.info']
    env.root = '/home/djangocon'
    env.src_root = join(env.root, 'src/djangocon')
    env.proj_root = join(env.src_root, 'djangocon')
    env.pip_file = join(env.src_root, 'requirements.txt')
    env.pid_file = '/tmp/djangocon.pid'
    env.deploy_dir = join(env.proj_root, 'deploy')
    env.gunicorn_config = join(env.deploy_dir, 'gunicorn.conf.py')
    env.nginx_config = join(env.deploy_dir, 'nginx.conf')
    env.nginx_dest = "/etc/nginx/conf.d/djangocon.conf"
    env.manage_py = join(env.proj_root, 'manage.py')

def staging():
    env.hosts = ['djangocon-staging@phaia.rdev.info']
    env.root = '/home/djangocon-staging'
    env.src_root = join(env.root, 'src/djangocon')
    env.proj_root = join(env.src_root, 'djangocon')
    env.pip_file = join(env.src_root, 'requirements.txt')
    env.pid_file = '/tmp/djangocon-staging.pid'
    env.deploy_dir = join(env.proj_root, 'deploy')
    env.gunicorn_config = join(env.deploy_dir, 'gunicorn.conf.py')
    env.nginx_config = join(env.deploy_dir, 'nginx.conf')
    env.nginx_dest = "/etc/nginx/conf.d/djangocon-staging.conf"
    env.manage_py = join(env.proj_root, 'manage.py')

def update():
   """Update source, update pip requirements, syncdb, restart server"""
   update_proj()
   update_reqs()
   link_settings()
   build_static_files()
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

def build_static_files():
    """Runs staticfiles build_static command to collect the various static media files of apps and Django"""
    ve_run('%s build_static --noinput'% env.manage_py)

def copy_nginx_config():
    sudo('cp %(nginx_config)s %(nginx_dest)s' % env)

def start_gunicorn():
    run('gunicorn djangocon.deploy.wsgi --config %(gunicorn_config)s -w 4 -p %(pid_file)s --daemon' % env)

def syncdb():
   """Run syncdb"""
   ve_run('%s syncdb --noinput' % env.manage_py)
   ve_run('%s migrate' % env.manage_py)

def ve_run(cmd):
   """
   Helper function.
   Runs a command using the virtualenv environment
   """
   require('root')
   return run('source %s/bin/activate; %s' % (env.root, cmd))
