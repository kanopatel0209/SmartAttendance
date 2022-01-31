"""
This module helps to manage environment settings.
"""

from os.path import exists
import environ


# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = environ.Path(__file__) - 3


env = environ.Env(
    # set casting, default value
    # DEBUG=(bool, )
)


# Take environment variables from .env file
env.read_env(BASE_DIR('SmartAttendance', 'Environ', 'Prod.env'))

# overwrite production environment variables to development environment variables.
if exists(BASE_DIR('SmartAttendance', 'Environ', 'Dev.env')):
  env.read_env(BASE_DIR('SmartAttendance', 'Environ', 'Dev.env'), overwrite=True)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG')

# environment settings
try:
  if DEBUG:
    from . import local_settings
  else:
    from . import prod_settings
except ImportError:
  pass

# import only ENV variables (uppercase variable)
from SmartAttendance.settings.base_settings import *
