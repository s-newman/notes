command = '/usr/bin/gunicorn'
pythonpath = '/opt/netbox/netbox'
bind = '127.0.0.1:8443'
workers = 3
user = 'www-data'
keyfile = '/opt/netbox/gunicorn-keyfile.pem'
certfile = '/opt/netbox/gunicorn-certfile.pem'
