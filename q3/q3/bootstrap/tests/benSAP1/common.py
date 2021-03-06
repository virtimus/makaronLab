from q3.api import *


def make8toB(name:str,parent:Module=None):
    m = parent.modAdd(name) if parent!=None else modvAdd(name).module()

    #for this mapper we have 8 1 bit singals on entry
    sformula = '=0'
    for i in range(0,8,1):
        m.iAdd(f'D{i}')
        sformula += f' | D{i}.value()<<{i}'

    # and one 8 bit signal on out
    m.oAdd('Y',size=8)

    # and one formula to make demulti
    m.setSigFormula('Y',sformula)
    return m


def makeBto8(name:str,parent:Module=None):
    #make root if parent is None
    m = parent.modAdd(name) if parent!=None else modvAdd(name).module()

    # and one in and 8 out
    m.iAdd('D',size=8)

    for i in range(0,8,1):
        m.oAdd(f'Y{i}')
        m.setSigFormula(f'Y{i}',f'=D[{i}]')
    return m

if __name__ == '__main__':
    make8toB('8toB')
    makeBto8('Bto8')