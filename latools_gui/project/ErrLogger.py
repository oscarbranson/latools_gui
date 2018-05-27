""" Stores and saves log """

import traceback
import time
import datetime
import logging
from functools import wraps

def initlog():
        logging.basicConfig(filename='Log-%s.log' % time.strftime('%Y-%m-%d-%H%M%S'), format='%(asctime)s: %(message)s', datefmt='%Y-%m-%d %I:%M:%S', level=logging.DEBUG)



def logged(func):
    @wraps(func)
    def logf(*args, **kwargs):
        logging.debug('Entering function %s with args %s and kwargs %s', func.__name__, args, kwargs)
        try:
            return func(*args, **kwargs)
            logging.debug('Exited function %s', func.__name__)
        except:
            logging.error('ERROR: Function %s triggered exception', func.__name__)
    return logf
        
