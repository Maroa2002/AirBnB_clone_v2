#!/usr/bin/python3
from fabric.api import local
from datetime import datetime
from os.path import exists


"""
generating a .tgz archive from contents of a folder
"""


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
