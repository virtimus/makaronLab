from q3.api import *

import q3.bootstrap.tests.benSAP1.common as cmn
import q3.bootstrap.tests.benSAP1.cpu_ALU_8bitAdder as alu
import q3.bootstrap.tests.benSAP1.cpu_D_latch_8bitreg_ei as dlatch8bitRegEI

import q3.bootstrap.tests.benSAP1.cpu_ALU_1bitAdder as cpuALU1bitAdder

#modv = modvAdd('')
#m = modv.module()

def makeALUABEI(name:str,parent:Module=None):
    #make root if parent is None
    m = parent.modAdd(name) if parent!=None else modvAdd(name).module()
    
    # add inputs/outputs
    nBI = m.iAdd('BI',size=8)
    nARIN = m.iAdd('ARIN')
    nAROUT = m.iAdd('AROUT')
    nBRIN = m.iAdd('BRIN')
    nBROUT = m.iAdd('BROUT')
    nALSUB = m.iAdd('ALSUB')
    nALOUT = m.iAdd('ALOUT')
    nCLK = m.iAdd('CLK')
    
    nBO = m.oAdd('BO',size=8)
    nRAI = m.oAdd('RAI',size=8)
    nRBI = m.oAdd('RBI',size=8)
    nALI = m.oAdd('ALI',size=8)
    nCO = m.oAdd('CO')
    nCIO = m.oAdd('CIO')
    nCZ = m.oAdd('CZ')
    
    mI = nBI.parent()
    mO = nBO.parent()
    
    mRegA = dlatch8bitRegEI.makeDlatch8bitregEI('registerA',m)
    mRegB = dlatch8bitRegEI.makeDlatch8bitregEI('registerB',m)
    mALU = alu.makeALU8bitAdder('ALU', m)
    
    mIBUS = cmn.makeBBUS('IBUS', m, inputsNo=3)
    
    nBI.c(mRegA.n('D'))
    nBI.c(mRegB.n('D'))
    
    #data flow connections
    mRegA.n('O').c(mIBUS.n('I0'))
    mRegB.n('O').c(mIBUS.n('I1'))
    mALU.n('S').c(mIBUS.n('I2'))
    
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