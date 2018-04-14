import logging
import os
from raven import Client

if os.getenv('PYTHON_ENV', 'development') == 'production':
    ravenClient = Client('https://099b35501c8c4d2fb6f26400c6c9bcef:0606a25c819d467d83d98c36f414bf54@sentry.io/1187304')
else:
    ravenClient = Client()
    logging.getLogger('raven').setLevel(logging.WARNING)