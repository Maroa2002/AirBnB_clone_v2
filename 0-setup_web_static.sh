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

# creating a symbolic link that is deleted if exists and recreated when script is rumsudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# giving ownership
sudo chown -R ubuntu:ubuntu /data/

# updating nginx configuration
nginx_config="/etc/nginx/sites-available/default"
sudo sed -i '/^\s*server_name _;/a\\n\
        location /hbnb_static/ {\n\
            alias /data/web_static/current/;\n\
        }\n' "$nginx_config"

# restarting nginx
sudo service nginx restart

exit 0
