"""
Gunicorn configuration file.

"""
import os

import gunicorn
from dotenv import load_dotenv

load_dotenv()

bind_ip = os.getenv('bind_ip', '0.0.0.0')
bind_port = os.getenv('bind_port', '5000')
bind = '{0}:{1}'.format(bind_ip, bind_port)
capture_output = True
accesslog = '/var/log/gunicorn/access.log'
errorlog = '/var/log/gunicorn/error.log'

# keyfile = os.getenv('ssl_key_path')
# certfile = os.getenv('ssl_cert_path')

workers = os.getenv('workers', 2)  # Number of worker processes (adjust based on your server’s CPU cores).
loglevel = os.getenv('LOG_LEVEL', 'INFO').lower()

gunicorn.SERVER_SOFTWARE = ''
