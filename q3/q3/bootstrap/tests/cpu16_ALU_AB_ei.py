from q3.api import *

import q3.bootstrap.tests.benSAP1.common as cmn
import q3.bootstrap.tests.benSAP1.cpu_ALU_8bitAdder as alu
import q3.bootstrap.tests.benSAP1.cpu_D_latch_8bitreg_ei as dlatch8bitRegEI

import q3.bootstrap.tests.benSAP1.cpu_ALU_1bitAdder as cpuALU1bitAdder
import q3.bootstrap.tests.benSAP1.cpu_OE_8bit_ei as oe
from q3.bootstrap.tests.cpu16_REG import makeReg16bitEI
#modv = modvAdd('')
#m = modv.module()

def makeALU16bitAdder(name:str,parent:Module=None):
    #make root if parent is None
    m = parent.modAdd(name) if parent!=None else modvAdd(name).module()
    tsize = 16
    # add inputs/outputs
    nA = m.iAdd('A',size=tsize)
    nB = m.iAdd('B',size=tsize)
    nCI = m.iAdd('CI')
    nSUB = m.iAdd('SUB')
    nENABLEB = m.iAdd('ENABLEB')
    nS = m.oAdd('S',size=tsize)
    nSI = m.oAdd('SI',size=tsize)
    nCO = m.oAdd('CO')
    nCIO = m.oAdd('CIO')
    mI = nA.parent()
    mO = nCO.parent() 
    
    mBto8b0 = cmn.makeStoN('Bto8b0',m, tsize)    
    mBto8b1 = cmn.makeStoN('Bto8b1',m, tsize)
    m8btoB0 = cmn.makeNtoS('8btoB0',m, tsize)
    m8btoB1 = cmn.makeNtoS('8btoB1',m, tsize)
    m8btoB2 = cmn.makeNtoS('8btoB2',m, tsize)
    
    mOE00 = oe.makeOE8bitEI('OE00', m)
    mOE01 = oe.makeOE8bitEI('OE01', m)
    nENABLEB.c(mOE00.n('ENABLEB'))
    nENABLEB.c(mOE01.n('ENABLEB'))
    
    mOE1 = oe.makeOE8bitEI('OE1', m)
    
    mI.n('A').c(mBto8b0.n('D'))
    mI.n('B').c(mBto8b1.n('D'))

      
    i=0
    pnod = nCI
    nX = -470
    nY = -360
    while i < tsize:
        xor = m.modAdd(f'XOR{i}',
                       impl = 'local:/XOR'
                       )
        nSUB.c(xor.n('B'))
        
        mod = cpuALU1bitAdder.makeALU1bitAdder(f'alu-1bitAdder{i}', m) 
        
        mBto8b0.n(f'Y{i}').c(mod.n('A'))
        mBto8b1.n(f'Y{i}').c(xor.n('A'))
        xor.n('Y').c(mod.n('B'))
        
        #mod.n('S').c(m8btoB0.n(f'D{i}'))
        if i>7:
            tn = mOE01.n(f'D{i-8}')
            if tn==None:
                print('')
            mod.n('S').c(tn)
            mOE01.n(f'O{i-8}').c(m8btoB0.n(f'D{i}'))
        else:            
            mod.n('S').c(mOE00.n(f'D{i}'))
            mOE00.n(f'O{i}').c(m8btoB0.n(f'D{i}'))

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

def makeBBUS(name:str,parent:Module=None,inputsNo=3, size = 16):
    #make root if parent is None
    m = parent.modAdd(name) if parent!=None else modvAdd(name).module()
    tsize = 16

    for i in range(0,inputsNo,1):
        m.iAdd(f'D{i}',size = size)

    m.oAdd('O',size = size)

    def calc(mimpl):
        m = mimpl.mdl()
        v = 0
        for i in range(0,inputsNo,1):
            v |= m.n(f'D{i}').value()
        m.n('O').intSignal().setValue(v)

    return m



def makeALUABEI(name:str,parent:Module=None):
    #make root if parent is None
    m = parent.modAdd(name) if parent!=None else modvAdd(name).module()
    tsize = 16
    
    # add inputs/outputs
    nBI = m.iAdd('BI',size=tsize)
    nARIN = m.iAdd('ARIN')
    nAROUT = m.iAdd('AROUT')
    nBRIN = m.iAdd('BRIN')
    nBROUT = m.iAdd('BROUT')
    nALSUB = m.iAdd('ALSUB')
    nALOUT = m.iAdd('ALOUT')
    nCLK = m.iAdd('CLK')
    
    nBO = m.oAdd('BO',size=tsize)
    nRAI = m.oAdd('RAI',size=tsize)
    nRBI = m.oAdd('RBI',size=tsize)
    nALI = m.oAdd('ALI',size=tsize)
    nCO = m.oAdd('CO')
    nCIO = m.oAdd('CIO')
    nCZ = m.oAdd('CZ')
    
    mI = nBI.parent()
    mO = nBO.parent()
    
    mRegA = makeReg16bitEI('registerA',m) #dlatch8bitRegEI.makeDlatch8bitregEI('registerA',m)
    mRegB = makeReg16bitEI('registerB',m) #dlatch8bitRegEI.makeDlatch8bitregEI('registerB',m)
    mALU = makeALU16bitAdder('ALU', m)
    
    mIBUS = makeBBUS('IBUS', m, inputsNo=3)
    
    nBI.c(mRegA.n('D'))
    nBI.c(mRegB.n('D'))
    
    #data flow connections
    mRegA.n('O').c(mIBUS.n('D0'))
    mRegB.n('O').c(mIBUS.n('D1'))
    mALU.n('S').c(mIBUS.n('D2'))
    
    #out data flow conns
    mIBUS.n('O').c(mO.n('BO'))
    mRegA.n('I').c(mO.n('RAI'))
    mRegB.n('I').c(mO.n('RBI'))
    mALU.n('SI').c(mO.n('ALI'))
    mALU.n('CO').c(mO.n('CO'))
    mALU.n('CIO').c(mO.n('CIO'))
    
    mNOT0 = m.modAdd('NOT0',
        impl = 'local:/NOT'
        )
    mNOT1 = m.modAdd('NOT1',
        impl = 'local:/NOT'
        )
    mNOT2 = m.modAdd('NOT2',
        impl = 'local:/NOT'
        )
    mNOT3 = m.modAdd('NOT3',
        impl = 'local:/NOT'
        )    
    mNOT4 = m.modAdd('NOT4',
        impl = 'local:/NOT'
        )            
    #input flags flows
    mI.n('ARIN').c(mNOT0.n('A'))
    mNOT0.n('Y').c(mRegA.n('LOADB'))
    mI.n('AROUT').c(mNOT1.n('A'))
    mNOT1.n('Y').c(mRegA.n('ENABLEB'))
    mI.n('BRIN').c(mNOT2.n('A'))
    mNOT2.n('Y').c(mRegB.n('LOADB'))
    mI.n('BROUT').c(mNOT3.n('A'))
    mNOT3.n('Y').c(mRegB.n('ENABLEB'))
    mI.n('ALSUB').c(mALU.n('SUB'))
    mI.n('ALOUT').c(mNOT4.n('A'))
    mNOT4.n('Y').c(mALU.n('ENABLEB'))
    mI.n('CLK').c(mRegA.n('CLK'))
    mI.n('CLK').c(mRegB.n('CLK'))
    
    #internal conns
    mRegA.n('I').c(mALU.n('A'))
    mRegB.n('I').c(mALU.n('B'))
    
    
    if m.isRoot(): #view needed for root only
        mI.setPos(-630.0,-190.0)
        mO.setPos(-260.0,-170.0)
        mRegA.setPos(-500.0,-280.0)
        mRegB.setPos(-500.0,-110.0)
        mALU.setPos(-390.0,-280.0)
        mIBUS.setPos(-390.0,-90.0)
        mNOT0.setPos(-560.0,-290.0)
        mNOT1.setPos(-560.0,-220.0)
        mNOT2.setPos(-560.0,-140.0)
        mNOT3.setPos(-560.0,-70.0)
        mNOT4.setPos(-450.0,-200.0)

        
    return m   

    
if __name__ == '__main__':
    makeALUABEI('cpu-ALU-AB-ei')    