from doctest import OutputChecker
from enum import Enum



class NodeIoType(Enum):
        INPUT = 0
        OUTPUT = 1
        DYNAMIC = 2
        @staticmethod
        def fromString(s:str):
                if s == 'O':
                        return NodeIoType.OUTPUT
                elif s == 'D':
                        return NodeIoType.DYNAMIC
                return NodeIoType.INPUT

        def oposite(self):
                if NodeIoType.INPUT == self:
                        return NodeIoType.OUTPUT
                if NodeIoType.OUTPUT == self:
                        return NodeIoType.INPUT
                return self