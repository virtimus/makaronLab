from q3.api import *

import q3.bootstrap.tests.benSAP1.common as cmn
import q3.bootstrap.tests.benSAP1.cpu_D_latch as dlatch
import q3.bootstrap.tests.benSAP1.cpu_OE_8bit_ei as oe

import q3.bootstrap.tests.benSAP1.cpu_ALU_1bitAdder as cpuALU1bitAdder

#modv = modvAdd('')
#m = modv.module()

def makeALU8bitAdder(name:str,parent:Module=None):
    #make root if parent is None
    m = parent.modAdd(name) if parent!=None else modvAdd(name).module()
    
    # add inputs/outputs
    nA = m.iAdd('A',size=8)
    nB = m.iAdd('B',size=8)
    nCI = m.iAdd('CI')
    nSUB = m.iAdd('SUB')
    nENABLEB = m.iAdd('ENABLEB')
    nS = m.oAdd('S',size=8)
    nSI = m.oAdd('SI',size=8)
    nCO = m.oAdd('CO')
    nCIO = m.oAdd('CIO')
    mI = nA.parent()
    mO = nCO.parent() 
    
    mBto8b0 = cmn.makeBto8('Bto8b0',m)    
    mBto8b1 = cmn.makeBto8('Bto8b1',m)
    m8btoB0 = cmn.make8toB('8btoB0',m)
    m8btoB1 = cmn.make8toB('8btoB1',m)
    
    mOE = oe.makeOE8bitEI('OE', m)
    nENABLEB.c(mOE.n('ENABLEB'))
    
    mOE1 = oe.makeOE8bitEI('OE1', m)
    
    mI.n('A').c(mBto8b0.n('D'))
    mI.n('B').c(mBto8b1.n('D'))

      
    i=0
    pnod = nCI
    nX = -470
    nY = -360
    while i < 8:
        xor = m.modAdd(f'XOR{i}',
                       impl = 'local:/XOR'
                       )
        nSUB.c(xor.n('B'))
        
        mod = cpuALU1bitAdder.makeALU1bitAdder(f'alu-1bitAdder{i}', m) 
        
        mBto8b0.n(f'Y{i}').c(mod.n('A'))
        mBto8b1.n(f'Y{i}').c(xor.n('A'))
        xor.n('Y').c(mod.n('B'))
        
        #mod.n('S').c(m8btoB0.n(f'D{i}'))
        
        mod.n('S').c(mOE.n(f'D{i}'))
        mOE.n(f'O{i}').c(m8btoB0.n(f'D{i}'))
        mod.n('S').c(m8btoB1.n(f'D{i}'))
        m8btoB1.n('Y').c(nSI)
        
        pnod.c(mod.n('CI'))
        pnod = mod.n('CO')
        if m.isRoot():
            nX = nX +70
            nY = nY +50
            mod.setPos(nX,nY)
            xor.setPos(nX-60,nY+20)
        if i==7:#last one to output CO
            mod.n('CO').c(mOE1.n('D0'))
            mOE1.n('O0').c(nCO)
            mod.n('CO').c(nCIO)
        i = i+1
        
    m8btoB0.n('Y').c(nS)
        
    if m.isRoot(): #view needed for root only
        mI.setPos(-630.0,-150.0)
        mO.setPos(270.0,-130.0)
        m8btoB0.setPos(170.0,-310.0)
        mBto8b0.setPos(-530.0,-310.0)
        mBto8b1.setPos(-530.0,-80.0)
        
    return m    

    
if __name__ == '__main__':
    makeALU8bitAdder('cpu-ALU-8bitAdder')