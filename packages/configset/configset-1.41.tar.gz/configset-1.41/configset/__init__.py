import imp
try:
	from . import __version__ as version
except:
	import __version__ as version
__version__ 	= version.version
__email__		= "licface@yahoo.com"
__author__		= "licface@yahoo.com"

from .configset import *