#!/usr/bin/python3
"""
Distributing an archive to a server
"""
from os.path import exists
from fabric.api import *


env.hosts = ["18.209.179.165", "52.91.117.26"]
env.user = "ubuntu"
env.key_filename = "~/.ssh/school"


def do_deploy(archive_path):
    """
    Distributes an archive to my web servers
    Args:
        archive_path: Path to the archive to be deployed
    Returns:
        True if all operations have been done correctly,
        otherwise returns False
    """

    if not exists(archive_path):
        return False

    try:
        # uploading the archive to /tmp/ directory of the web server
        put(archive_path, "/tmp/")

        timestamp = archive_path.split('.')[0][-14:]
        sudo('mkdir -p \
                /data/web_static/releases/web_static_{}/'
             .format(timestamp))

        # Uncompress archive, delete archive, Move files into Host
        # web_static then remove the src web_static dir
        sudo('tar -vxzf /tmp/web_static_{}.tgz -C \
            /data/web_static/releases/web_static_{}/'
             .format(timestamp, timestamp))

        sudo('rm /tmp/web_static_{}.tgz'.format(timestamp))

        sudo('mv /data/web_static/releases/web_static_{}/web_static/* \
            /data/web_static/releases/web_static_{}/'
             .format(timestamp, timestamp))

        sudo('rm -rf \
            /data/web_static/releases/web_static_{}/web_static'
             .format(timestamp))

        # Delete pre-existing sym link and re-establish
        sudo('rm -rf /data/web_static/current')

        sudo('ln -s /data/web_static/releases/web_static_{}/ \
            /data/web_static/current'.format(timestamp))

        return True
    except:
        return False

