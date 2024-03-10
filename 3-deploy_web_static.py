#!/usr/bin/python3
"""
Full deployment
"""
from os.path import exists
from fabric.api import put, sudo, env


env.hosts = ["18.209.179.165", "52.91.117.26"]
env.user = "ubuntu"


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder
    Returns:
        Archive path if successful, None otherwise
    """

    # creating versions folder if doesnt exist
    if not exists("versions"):
        local("mkdir -p versions")

    # current timestamp for the archive name
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")

    # archive name
    archive_name = "web_static_{}.tgz".format(timestamp)

    # archive path
    archive_path = "versions/{}".format(archive_name)

    # compressing the web_static folder into a .tgz archive
    result = local("tar -cvzf {} web_static".format(archive_path))

    # check if compression was successful
    if result.succeeded:
        return archive_path
    else:
        return None


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
    except Exception as e:
        print(e)
        return False


def deploy():
    """
    Creates and distributes an archive to your web servers
    Returns:
        True if all operations have been done correctly,
        otherwise returns False
    """
    # Create the archive
    archive_path = do_pack()

    # Return False if no archive has been created
    if not archive_path:
        return False

    # Deploy the archive
    return do_deploy(archive_path)
