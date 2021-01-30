from ... import consts, prop, orientation, direction, colors

from enum import Enum

class ValueType(Enum):
    BOOL = (1,colors.C.BOOLSIGNALOFF, colors.C.BOOLSIGNALON, 'BOOL')
    INT = (2,colors.C.INTEGERSIGNALOFF,colors.C.INTEGERSIGNALON,'INT')
    FLOAT = (3,colors.C.FLOATSIGNALOFF, colors.C.FLOATSIGNALON,'FLOAT')
    BYTE =  (4, colors.C.BYTESIGNALOFF, colors.C.BYTESIGNALON,'BYTE')
    WORD64 = (5, colors.C.WORD64SIGNALOFF, colors.C.WORD64SIGNALON,'WORD64')

    def __init__(self, number, colorSigOff, colorSigOn, strin):
        self._number = number
        self._colorSigOn = colorSigOn
        self._colorSigOff = colorSigOff
        self._string = strin

    @classmethod
    def fromInt(cls, ii):
        if ii == 1:
            return ValueType.BOOL
        if ii == 1:
            return ValueType.INT
        if ii == 1:
            return ValueType.FLOAT
        if ii == 1:
            return ValueType.BYTE
        if ii == 1:
            return ValueType.WORD64
        return None

    

        

    def number(self):
        return self._number
    
    def colorSigOn(self):
        return self._colorSigOn.qColor()
    
    def colorSigOff(self):
        return self._colorSigOff.qColor()

    def toString(self):
        return self._string

    def toInt(self):
        return self.number()