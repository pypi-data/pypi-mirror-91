import sys
import time
import calendar
import psutil




def platform():
  return sys.platform
def timestamp():
  t=time.gmtime()
  tc=calendar.timegm(t)
  return tc
def py():
  return sys.version()
def __running__(processName):
    '''
    Check if there is any running process that contains the given name processName.
    '''
    for proc in psutil.process_iter():
        try:
            if processName.lower() in proc.name().lower():
              return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
          pass
    return False