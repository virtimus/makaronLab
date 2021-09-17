from q3.api import *
from q3.bootstrap.tests.cpu16_ALU_AB_ei import makeBBUS,makeALUABEI
from q3.bootstrap.tests.cpu16_PC_ei import makePCEI
from q3.bootstrap.tests.cpu16_RAM_ei import makeRAMEI
from q3.bootstrap.tests.cpu16_REG import makeReg16bitEI

def makeCPU16(name:str,parent:Module=None):
    #make root if parent is None
    
    m = parent.modAdd(name) if parent!=None else modvAdd(name).module()
    nCLK = m.iAdd('CLK')
    a = {
        'HOLD',
        'UNC0',
        'RAM-IN',
        'RAM-OUT',
        'IR-IN',
        'IR-OUT',
        'AR-IN',
        'AR-OUT',
        'AL-OUT',
        'AL-SUB',
        'BR-IN',
        'BR-OUT',
        'UNC1',
        'PC-INC',
        'PC-JUMP',
        'PC-OUT',
        'PC-OUTD',
        'RST',
        'UNC2',
        'PRMODE',
        'UNC3',
        'UNC4',
        'SP-INC',
        'SP-DEC',
        'SP-JUMP',
        'SP-OUT',
        'SP-OUTD',
        'ML-IN',
        'ML-OUT',
        'ML-OUTD'        
    }
    nIa = {}
    for k in a:
        nIa[k]=m.iAdd(k)

    #outputs
    nADRO = m.oAdd('ADRBUS-O', size = 16)
    nDTAO = m.oAdd('DTABUS-O', size = 16)

    o = {
        'ML-O',
        'ML-DO',
        'ML-I',
        'IR-O',
        'IR-I',
        'RAM-O',
        'RAM-I',
        'PC-O',
        'PC-DO',
        'PC-I', 
        'SP-O',
        'SP-DO',
        'SP-I',
        'AL-BO',
        'AL-RAI',
        'AL-RBI',
        'AL-ALI',
     
    }
    nOa = {}
    for k in o:
        nOa[k]=m.oAdd(k, size = 16)

    nALCO = m.oAdd('AL-CO')
    nALCIO = m.oAdd('AL-CIO')
    nALCZ = m.oAdd('AL-CZ') 

    mADRBUS = makeBBUS('AddressBus', m, inputsNo=6)
    mDTABUS = makeBBUS('DataBus', m, inputsNo=6)

    mPC = makePCEI('PC',m,spc=False,asB=False)
    mSP = makePCEI('SP',m,spc=True,asB=False)
    mALU = makeALUABEI('ALU',m)
    mIREG = makeReg16bitEI('IREG',m,asB=False)
    mIR = mIREG
    mML = makeReg16bitEI('ML',m,dataOutput=True,asB=False)
    mRAM = makeRAMEI('RAM',m)

    nCLK.c(mIREG.n('CLK'))
    nCLK.c(mML.n('CLK'))
    nCLK.c(mALU.n('CLK'))
    nCLK.c(mPC.n('CLK'))
    nCLK.c(mSP.n('CLK'))
    nCLK.c(mRAM.n('CLK'))
    #'''
    #control inputs
    #nIa['HOLD']=None
    #nIa['UNC0']=None

    nIa['RAM-IN'].c(mRAM.n('RAMIN'))
    nIa['RAM-OUT'].c(mRAM.n('RAMOUT'))
    nIa['IR-IN'].c(mIREG.n('LOAD'))
    nIa['IR-OUT'].c(mIREG.n('ENABLE'))
    nIa['AR-IN'].c(mALU.n('ARIN'))
    nIa['AR-OUT'].c(mALU.n('AROUT'))
    nIa['AL-OUT'].c(mALU.n('ALOUT'))
    nIa['AL-SUB'].c(mALU.n('ALSUB'))
    nIa['BR-IN'].c(mALU.n('BRIN'))
    nIa['BR-OUT'].c(mALU.n('BROUT'))
    #nIa['UNC1']=None
    nIa['PC-INC'].c(mPC.n('INC'))
    nIa['PC-JUMP'].c(mPC.n('LOAD'))
    nIa['PC-OUT'].c(mPC.n('ENABLE'))
    nIa['PC-OUTD'].c(mPC.n('ENABLED'))
    nIa['RST'].c(mRAM.n('RST'))
    nIa['RST'].c(mPC.n('CLEAR'))
    nIa['RST'].c(mSP.n('CLEAR'))
    #nIa['UNC2']=None
    nIa['PRMODE'].c(mRAM.n('PRMOD'))
    #nIa['UNC3']=None
    #nIa['UNC4']=None
    nIa['SP-INC'].c(mSP.n('INC'))
    nIa['SP-DEC'].c(mSP.n('DEC'))
    nIa['SP-JUMP'].c(mSP.n('LOAD'))
    nIa['SP-OUT'].c(mSP.n('ENABLE'))
    nIa['SP-OUTD'].c(mSP.n('ENABLED'))
    nIa['ML-IN'].c(mML.n('LOAD'))
    nIa['ML-OUT'].c(mML.n('ENABLE'))
    nIa['ML-OUTD'].c(mML.n('ENABLED'))

    #connections (data)
    mDTABUS.n('O').c(mALU.n('BI'))
    mDTABUS.n('O').c(mIREG.n('D'))
    mDTABUS.n('O').c(mML.n('D'))
    mDTABUS.n('O').c(mPC.n('D'))
    mDTABUS.n('O').c(mSP.n('D'))
    mDTABUS.n('O').c(mRAM.n('D'))

    #into dtabus
    mALU.n('BO').c(mDTABUS.n('D0'))
    mPC.n('DO').c(mDTABUS.n('D1'))
    mSP.n('DO').c(mDTABUS.n('D2'))
    mRAM.n('O').c(mDTABUS.n('D3'))
    mML.n('DO').c(mDTABUS.n('D4'))
    

    #from adrbus into RAM address
    mADRBUS.n('O').c(mRAM.n('A'))

    #into adrbus
    mPC.n('O').c(mADRBUS.n('D0'))
    mSP.n('O').c(mADRBUS.n('D1'))
    mML.n('O').c(mADRBUS.n('D2'))

    #outputs
    mADRBUS.n('O').c(nADRO)
    mDTABUS.n('O').c(nDTAO)
    mML.n('O').c(nOa['ML-O'])
    mML.n('DO').c(nOa['ML-DO'])
    mML.n('I').c(nOa['ML-I'])
    mIR.n('O').c(nOa['IR-O'])
    mIR.n('I').c(nOa['IR-I'])
    mRAM.n('O').c(nOa['RAM-O'])
    mRAM.n('I').c(nOa['RAM-I'])
    mPC.n('O').c(nOa['PC-O'])
    mPC.n('DO').c(nOa['PC-DO'])
    mPC.n('I').c(nOa['PC-I']) 
    mSP.n('O').c(nOa['SP-O'])
    mSP.n('DO').c(nOa['SP-DO'])
    mSP.n('I').c(nOa['SP-I'])
    mALU.n('BO').c(nOa['AL-BO'])
    mALU.n('RAI').c(nOa['AL-RAI'])
    mALU.n('RBI').c(nOa['AL-RBI'])
    mALU.n('ALI').c(nOa['AL-ALI'])

    mALU.n('CO').c(nALCO)     
    mALU.n('CIO').c(nALCIO)
    mALU.n('CZ').c(nALCZ)

    if m.isRoot():
        mIREG.setPos(100.0,-130.0)
        mALU.setPos(100.0,40.0)
        mDTABUS.setPos(-20.0,-40.0)
        mSP.setPos(-220.0,110.0)
        mPC.setPos(-220.0,-100.0)
        mADRBUS.setPos(-440.0,-150.0)
        m.mod('moduleInputs').setPos(-600.0,0.0)
        mRAM.setPos(-440.0,70.0)

    return m

if __name__ == '__main__':
    makeCPU16('cpu16')