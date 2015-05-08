import os

def to_bool(val):
     if isinstance(val, basestring):
         if val == '1' or val.lower() == 'true':
             return True
         return False
     return bool(val)
  
port = int(os.environ.get('PORT', 5000))

# Debug is unsafe, so the default should be debug==False
environment = os.environ.get('HEROKU_ENVIRONMENT', 'LOCAL')

if environment == 'LOCAL':
    print "Running locally with debug=True"
    debug = True
else:
    debug = to_bool(os.environ.get('APP_MODE_DEBUG', False))
