
from datetime import datetime
from datetime import timedelta
from time import sleep

class Timer:
    def __init__(self):
        self._startTime = datetime.now()

    def toMilis(self, t):
        ms = (t.days * 24 * 60 * 60 + t.seconds) * 1000 + t.microseconds / 1000.0
        return round(ms)

    def ms(self,number=1):
        #return number*self._startTime.microsecond/1000 #!!
        return timedelta(milliseconds=number)

    def now(self):
        return  datetime.now()

    def startTime(self):
        return self._startTime

    @staticmethod
    def sleepMs(ms:int):
        sleep(ms/1000)

    def millisDelta(self, toTime=None):
        fr = toTime if toTime != None else self.now()
        dt = fr - self._startTime
        ms = self.toMilis(dt)
        return ms