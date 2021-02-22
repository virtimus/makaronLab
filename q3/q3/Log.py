
import logging
import sys

logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

class Log:
    def __init__(self,name:str):
        tlog = logging.getLogger(name)
        thandler = logging.StreamHandler(sys.stdout)
        tformatter = logging.Formatter('%(asctime)s/%(name)s/%(levelname)s: %(message)s')
        thandler.setFormatter(tformatter)
        tlog.addHandler(thandler)
        tlog.setLevel(logging.INFO)
        self._impl = tlog

    def warn(
            self,
            msg,
            *args,
            **kwargs) -> None:
            return self._impl.warn(msg,*args,**kwargs) 
    def error(
            self,
            msg,
            *args,
            **kwargs) -> None:
            return self._impl.error(msg,*args,**kwargs)  
    def info(
            self,
            msg,
            *args,
            **kwargs) -> None:
            return self._impl.info(msg,*args,**kwargs)     