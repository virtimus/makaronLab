
from traceback import print_stack
from q3.api import *

# Ben is starting logging output from 6502 as binary addr/data, hex addr, R/W flag and hex data

#first add new rootModule with view

def makeLUT(name:str,parent:Module,lutdef):
    m = parent.modAdd(name) if parent!=None else modAdd(name)

    iCount = 0
    oCount = 0
    lut = []
    for s in lutdef:
        e = s.split(':')
        iCount = len(e[0])
        oCount = len(e[1])
        lut.append(e)


    for i in range(0,iCount,1):
        m.iAdd(f'D{i}')

    for i in range(0,oCount,1):
        m.oAdd(f'Y{i}')

    def calc(mimpl):
        m = mimpl.mdl()
        mProps = m.props()

        for i in range(0,len(lut),1):
            bmatch = True
            e = lut[i]
            for j in range(0,iCount,1):
                iv = '1' if m.n(f'D{j}').value() else '0'
                if not (iv==e[0][j] or e[0][j]=='?'):
                    bmatch = False
                    break
            if bmatch:
                for j in range(0,oCount,1):
                    v = True if e[1][j]=='1' else False
                    m.n(f'Y{j}').intSignal().setValue(v)
                break


    m.setCalc(calc)

    return m

def makeFULLADDER(name:str,parent:Module=None):
    #make root if parent is None
    m = parent.modAdd(name) if parent!=None else modAdd(name)
    
    iA = m.iAdd('A')
    iB = m.iAdd('B')
    iC = m.iAdd('CI')
    oS = m.oAdd('S')
    oC = m.oAdd('CO')
    
    mXOR4 = m.modAdd('XOR0',
        impl = 'local:/XOR4'
        )
    
    iA.con(mXOR4.nod('A'))
    iB.con(mXOR4.nod('B'))
    iC.con(mXOR4.nod('C'))
    mXOR4.nod('Y').con(oS)

    mLUT0 = makeLUT('LUT0',m,[
            '11?:1',
            '1?1:1',
            '?11:1',
            '?00:0',
            '0?0:0',
            '00?:0'
            ]
        )

    if m.isRoot():
        mLUT0.setPos(70.0,100.0)

    iA.con(mLUT0.n('D0'))
    iB.con(mLUT0.n('D1'))
    iC.con(mLUT0.n('D2'))
    mLUT0.n('Y0').c(oC)    
    
    return m
    
if __name__ == '__main__':
    makeFULLADDER('L2 - HARDWARE MODELING USING VERILOG by IIT KHARAGPUR NPTEL')