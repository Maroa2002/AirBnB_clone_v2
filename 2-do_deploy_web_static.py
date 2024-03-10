#!/usr/bin/python3
"""
Distributing an archive to a server
"""
from os.path import exists
from fabric.api import put, sudo


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

        archive_name = archive_path.split('/')[-1]
        folder_name = archive_name.split('.')[0]

        # Uncompress the archive to the folder
        # /data/web_static/releases/<archive filename without extension>
        sudo("mkdir -p \
             /data/web_static/releases/{}".format(folder_name))
        sudo("tar -vxzf \
             /tmp/{} -C /data/web_static/releases/{}".format(archive_name,
                                                             folder_name))

        # Delete the archive from the web server
        sudo("rm /tmp/{}".format(archive_name))

        sudo("mv /data/web_static/releases/{}/web_static/* \
            /data/web_static/releases/{}"
             .format(folder_name, folder_name))
        sudo("rm -rf \
            /data/web_static/releases/{}/web_static"
             .format(folder_name))

        # Delete the symbolic link /data/web_static/current from the web server
        sudo("rm -rf /data/web_static/current")

        # Create a new symbolic link /data/web_static/current on the web server
        # Linked to the new version of my code
        # (/data/web_static/releases/<archive filename without extension>)
        sudo("ln -s /data/web_static/releases/{}/\
             /data/web_static/current".format(folder_name))

        print("New version deployed!")
        return True
    except as e:
        print(e)
        return False
