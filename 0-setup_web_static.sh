#!/usr/bin/env bash
# setting up my web servers for the deployment of web_static

# installing nginx if not already installed
if ! [ -x "$(command -v nginx)" ];then
        sudo apt-get update
        sudo apt-get -y install nginx
fi

# starting nginx
sudo service nginx start

# creating the necessary  folders
sudo mkdir -p /data/web_static/releases/test/ /data/web_static/shared/

fake_html="
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>"

# creating a fake html file
echo "$fake_html" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# creating a symbolic link that is deleted if exists and recreated when script is run
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# giving ownership
sudo chown -R ubuntu:ubuntu /data/

# updating nginx configuration
if ! sudo grep -q "alias /data/web_static/current/;" /etc/nginx/sites-enabled/default; then
    sudo sed -i "\#server_name _;#a \\
        location /hbnb_static { \\
            alias /data/web_static/current/; \\
        } \\
        "  /etc/nginx/sites-enabled/default
fi

# restarting nginx
sudo service nginx restart

exit 0
