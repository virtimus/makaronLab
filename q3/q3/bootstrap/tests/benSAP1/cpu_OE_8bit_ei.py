from q3.api import *


def makeOE8bitEI(name:str,parent:Module=None):
    #make root if parent is None
    m = parent.modAdd(name) if parent!=None else modvAdd(name).module()

    nENABLEB = m.iAdd('ENABLEB')
    mNOT0 = m.modAdd('NOT0',
        impl = 'local:/NOT'
        )
    nENABLEB.c(mNOT0.n('A'))

    #view
    mNOT0.setPos(-170.0,-250.0)

    nDA = {}
    nOA = {}
    nIA = {}

    # separate loop for io as we want to have o and I in group
    for i in range(0,8,1):
        dname = f'D{i}'
        oname = f'O{i}'
        nD = m.iAdd(dname)
        nDA[dname] = nD 
        nO = m.oAdd(oname)
        nOA[oname] = nO


    mANDA = {}
    x = 200
    y = -400
    w=20
    h=60
    for i in range(0,8,1):
        dname = f'D{i}'
        oname = f'O{i}'
        iname = f'I{i}'
        nD = nDA[dname]  
        nO = nOA[oname]
        nI = m.oAdd(iname)
        nIA[oname] = nI

        andname = f'AND{i}'
        mAND = m.modAdd(andname,
            impl = 'local:/AND'
            )
        mANDA[andname] = mAND

        #view
        mAND.setPos(x-(w*i),y+(h*i))

        #connect
        mNOT0.n('Y').c(mAND.n('A'))
        nD.c(mAND.n('B'))
        mAND.n('Y').c(nO)
        #internal signals
        #currently have to have driveSignal connecting i to o
        if nD.driveSignal()==None:
            nD.setDriveSignal(nD.intSignal())
        nD.connect(nI)
    return m



if __name__ == '__main__':
    makeOE8bitEI('cpu-OE-8bit-ei')