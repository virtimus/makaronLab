
from .valuetype import ValueType
from . import consts

class IoNodeFlags:

    def canChangeName(self):
        return self._canChangeName

    def canHoldValues(self):
        return [ValueType.BOOL]

    def __init__(self,
            canChangeName=False,
            canHoldBool= True,
            canHoldInt = False,
            canHoldFloat = False,
            canHoldByte = False,
            canHoldWord64 = False,
            canHoldAllValues = False,
            max = consts.MAX_PINS, 
            min = 0   
            ):
        self._canHoldAllValues = canHoldAllValues
        self._canChangeName = canChangeName
        self._canHoldBool = canHoldBool
        self._canHoldInt =  canHoldInt
        self._canHoldFloat = canHoldFloat
        self._canHoldByte  = canHoldByte
        self._canHoldWord64 = canHoldWord64
        self._max = max
        self._min = min

    def min(self):
        return self._min

    def setIfMin(self, min):
        if self._max<min:
            return
        self._min = min

    def max(self):
        return self._max

    def setIfMax(self, max):
        if self._min>max:
            return
        self._max = max


    def valueTypeAllowed(self, vType:ValueType):
        #value_type_allowed(uint8_t const a_flags, ValueType const a_type)
        if self._canHoldAllValues:
            return True
        if vType == ValueType.BOOL:
            return self._canHoldBool
        if vType == ValueType.INT:
            return self._canHoldInt
        if vType == ValueType.FLOAT:
            return self._canHoldFloat
        if vType == ValueType.BYTE:
            return self._canHoldByte
        if vType == ValueType.WORD64:
            return self._canHoldWord64
        assert(False)

    def firstAvailableType(self):
        if (self._canHoldBool):
            return ValueType.BOOL
        if (self._canHoldInt):
            return ValueType.INT
        if (self._canHoldFloat):
            return ValueType.FLOAT
        if (self._canHoldByte):
            return ValueType.BYTE
        if (self._canHoldWord64):
            return ValueType.WORD64
        return ValueType.BOOL 

    @staticmethod 
    def defaultFlags():
        return IoNodeFlags(canChangeName=True,canHoldAllValues=True)