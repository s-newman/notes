ALLOWED_HOSTS = ['netbox.ritsec.club', 'localhost']

# PostgreSQL database configuration.
DATABASE = {
    'NAME': 'netbox',         # Database name
    'USER': 'netbox',         # PostgreSQL username
    'PASSWORD': 'changeme',   # PostgreSQL password
    'HOST': 'localhost',      # Database server
    'PORT': '',               # Database port (leave blank for default)
}

# Replace this with a value at least 50 characters long. You can use the script
# at netbox/generate_secret_key.py for this.
SECRET_KEY = 'changeme'

# Banner settings
BANNER_BOTTOM = 'RITSEC - https://www.ritsec.club'
BANNER_LOGIN = 'The RITSEC Netbox instance is publicly accessible without authentication. If you would like to make modifications, please contact an Operations Program member to get an account.'  # noqa
