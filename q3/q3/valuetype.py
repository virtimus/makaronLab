from . import consts, prop, direction
from .ui import orientation, colors

import q3.console as c

#print(f'dirq3:{dir(q3)}')

from enum import Enum

class ValueType:
    # moved down

    def __new__(cls, *args, **kwargs):
        result = object.__new__(cls)
        result._args = args
        result._kwargs = kwargs
        return result

    def __init__(self, number, size, colorSigOff, colorSigOn, strin=None):
        self._number = number
        if (callable(colorSigOff)):
            print('trace')
        self._colorSigOn = colorSigOn
        self._colorSigOff = colorSigOff
        self._sizeTmp = None
        size = c.handleArg(self,'size',
            value = size,
            required = True,
            desc = 'Size of value'
        )
        if strin == None:
            strin == f'({size}b)'
        self._string = strin
        self._size = size
        self._value = False if size == 1 else 0
        self._parent = None

    # central point for signal values change
    # currently no validation on get and very liitle on set (fits fixed to True)
    # handy for development but to be fixed in target sol !TODO!
    def value(self):
        return self._value

    def setValue(self, newVal):
        if newVal != self._value: # is there a real change ?
            if self.fits(newVal): # why newVal != None and was there ?
                prevVal = self._value 
                self._value = newVal
                if self._parent != None:
                    self._parent.onValueChanged(prevVal, self._value)
            else:
                assert False, f'Value:{newVal} overflows valueType size:{self.size()}'

    def setParentSignal(self, parent):
        self._parent = parent

    ''' value None (disconnected)
    def resetValue(self):
        prevValue = self._value
        if isinstance(self._value, bool):
            self._value = False
        else:
            self._value = 0
    '''

    def asUInt(self):
        result = self._value 
        if self.size()<2:
            result = 1 if self._value else 0
        return result

    @classmethod
    def fromInt(cls, ii):
        if ii == 1:
            return ValueType.BOOL
        if ii == 2:
            return ValueType.INT
        #if ii == 3:
        #    return ValueType.FLOAT
        if ii == 4:
            return ValueType.BYTE
        if ii == 5:
            return ValueType.WORD64
        return None

    @staticmethod
    def fromSize(size:int):
        result = ValueType.BOOL
        if size > 63:
            result = ValueType.WORD64
        elif size > 8:
            result = ValueType.INT
        elif size > 1:
            result = ValueType.BYTE
        return result

    def toSize(self):
        tsize = 32
        if self == ValueType.BOOL:
            tsize = 1
        elif self == ValueType.BYTE:
            tsize = 8
        elif self == ValueType.WORD64:
            tsize = 64
        return tsize

    def size(self):
        return self._size

    #@deprecated - to be deleted after cleaning addinput/io etc
    def setSizeTmp(self, nsize:int):
        self._sizeTmp = nsize 

    def fits(self,value):
        return True    

    def typeIndex(self):
        return self._number
    
    def colorSigOn(self):
        return self._colorSigOn.qColor()
    
    def colorSigOff(self):
        return self._colorSigOff.qColor()

    def toString(self):
        return self._string

    #def toInt(self):
    #    return self.number()

ValueType.BOOL = ValueType(1,1,colors.C.BOOLSIGNALOFF, colors.C.BOOLSIGNALON, 'BOOL')
ValueType.INT = ValueType(2,63,colors.C.INTEGERSIGNALOFF,colors.C.INTEGERSIGNALON,'INT')
#    FLOAT = (3,colors.C.FLOATSIGNALOFF, colors.C.FLOATSIGNALON,'FLOAT')
ValueType.BYTE =  ValueType(4,8, colors.C.BYTESIGNALOFF, colors.C.BYTESIGNALON,'BYTE')
ValueType.WORD64 = ValueType(5,64, colors.C.WORD64SIGNALOFF, colors.C.WORD64SIGNALON,'WORD64')