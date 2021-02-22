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


