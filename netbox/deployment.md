# Netbox deployment steps

This was written using the Ubuntu 18.04 AMI on AWS.

## Hardware
Create a new EC2 instance of flavor t3a.small, give it 20 G of disk, and ports
22, 65432, 80, and 443 open on the security group. Then create a new elastic IP
and associate it with the instance. Finally, create an A record to point to the
elastic IP with a name of `netbox.ritsec.club`.

## Pre-deployment prep
Hostname:
```shell
sudo hostnamectl set-hostname netbox
echo "127.0.0.1 localhost" | sudo tee /etc/hosts
echo "127.0.1.1 netbox" | sudo tee -a /etc/hosts
```

Reconfigure ssh port:
```shell
sudo sed -i 's/#Port 22/Port 65432/g' /etc/ssh/sshd_config
sudo systemctl restart ssh
```

Exit the box and remove port 22 from the security group.

## Deployment
Prep certbot repos
```shell
sudo apt-get update && sudo apt-get install -y software-properties-common
sudo add-apt-repository universe
sudo add-apt-repository ppa:certbot/certbot
```

Install required packages
```shell
sudo apt-get update && sudo apt-get install -y \
    postgresql \
    libpq-dev \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    libxml2-dev \
    libxslt1-dev \
    libffi-dev \
    graphviz \
    libpq-dev \
    libssl-dev \
    zlib1g-dev \
    nginx \
    supervisor \
    certbot \
    python-certbot-nginx
```

Start and enable postgres
```shell
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

Set up the database - make sure to change the password though!
```shell
sudo -u postgres psql -c "CREATE DATABASE netbox;"
sudo -u postgres psql -c "CREATE USER netbox WITH PASSWORD 'changeme';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE netbox TO netbox;"
```

Download the release
```shell
wget https://github.com/digitalocean/netbox/archive/v2.5.12.tar.gz
sudo tar -xzf v2.5.12.tar.gz -C /opt
cd /opt
sudo ln -s netbox-2.5.12/ netbox
cd /opt/netbox
```

Install pip requirements
```shell
sudo pip3 install -r requirements.txt
cd netbox/netbox/
# Copy over configuration.py to this file
sudo vim configuration.py
# Make sure to change the database password and the secret key
```

Run manage.py scripts
```shell
cd /opt/netbox/netbox
sudo python3 manage.py migrate
# YOU NEED TO TYPE FOR THE FOLLOWING COMMAND!
sudo python3 manage.py createsuperuser
# YOU NEED TO TYPE FOR THE ABOVE COMMAND!
sudo python3 manage.py collectstatic --no-input
sudo python3 manage.py loaddata initial_data
```

Configure nginx
```shell
sudo rm -rf /etc/nginx/sites-*
# copy over nginx.conf
sudo vim /etc/nginx/nginx.conf
# copy over 50-netbox.conf
sudo vim /etc/nginx/conf.d/50-netbox.conf
```

Get nginx cert
```shell
sudo certbot --nginx certonly --register-unsafely-without-email
# Add renewal to certbot
sudo crontab -e
#0 3 * * * certbot renew # Renew certs every day at 3:00 AM
sudo systemctl restart nginx
sudo systemctl enable nginx
```

Set up gunicorn
```shell
# Geerate
sudo openssl req -x509 -newkey rsa:4096 -days 3650 -nodes \
    -keyout /opt/netbox/gunicorn-keyfile.pem \
    -out /opt/netbox/gunicorn-certfile.pem
sudo pip3 install gunicorn
# copy over gunicorn_config.py
sudo vim /opt/netbox/gunicorn_config.py
```

Set permissions on netbox directory
```
sudo chown -R www-data:www-data /opt/netbox*
```

Set up supervisord
```shell
# copy over netbox.conf
sudo vim /etc/supervisor/conf.d/netbox.conf
sudo systemctl restart supervisor
sudo systemctl enable supervisor
```