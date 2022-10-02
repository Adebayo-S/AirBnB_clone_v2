#!/usr/bin/python3
"""
 that distributes an archive to your web servers,
 using the function do_deploy

 run:
 fab -f 2-do_deploy_web_static.py do_deploy:archive_path=
 versions/web_static_20170315003959.tgz -i my_ssh_private_key -u
 ubuntu
"""
from fabric.api import env, put, run
import os.path

env.hosts = ['3.229.122.175', '35.171.146.79']
env.user = "ubuntu"
env.key_filename = '~/.ssh/school'
# env.use_ssh_config


def do_deploy(archive_path):
    """ deploy to a web server """
    if not os.path.exists(archive_path):
        return False
    try:
        file = archive_path.split("/")[-1]
        name = file.split(".")[0]
        path = "/data/web_static/releases/{}/".format(name)
        put(archive_path, "/tmp/")
        run('mkdir -p {}{}/'.format(path, name))
        run('tar -xzf /tmp/{} -C {}{'.format(file, path))
        run('rm /tmp/{}'.format(file))
        run('mv {}/web_static/* {}/'.format(path, path))
        run("rm -rf {}web_static".format(path))
        run('rm -rf /data/web_static/current')
        run("ln -s {} /data/web_static/current".format(path))
        run('echo "New version deployed!"')
        return True
    except BaseException:
        run('echo "wahala!"')
        return False
