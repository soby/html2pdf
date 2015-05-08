import os

def to_bool(val):
     if isinstance(val, basestring):
         if val == '1' or val.lower() == 'true':
             return True
         return False
     return bool(val)
  
port = int(os.environ.get('PORT', 5000))

