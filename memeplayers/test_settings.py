# memeplayers/test_settings.py

from .settings import *

# Disable throttling for tests
REST_FRAMEWORK['DEFAULT_THROTTLE_CLASSES'] = []