""" Stores and saves log """

import traceback
import time
import datetime
import logging
from functools import wraps

def initlog():
	logging.basicConfig(filename='logs/Log-%s.log' % time.strftime('%Y-%m-%d-%H%M%S'), format='%(asctime)s: %(message)s', datefmt='%Y-%m-%d %I:%M:%S', level=logging.DEBUG)



def logged(func):
	@wraps(func)
	def logf(self, *args, **kwargs):             
		logging.critical('Entering function '+func.__qualname__+' with args {} and kwargs {}'.format(args, kwargs))
		try:
			r = func(self, *args, **kwargs)
			logging.debug('Exited function %s', func.__qualname__)
			return r
		except TypeError:
                        try:
                                logging.debug('Retrying with zero-length args')
                                r = func(self)
                                return r
                        except: raise
		except:
			logging.exception('ERROR: Function %s triggered exception', func.__qualname__)
	
	return logf


