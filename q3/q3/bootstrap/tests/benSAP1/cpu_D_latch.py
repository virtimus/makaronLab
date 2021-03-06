from q3.api import *



def makeDLatch(name:str,parent:Module=None):
    #make root if parent is None
    m = parent.modAdd(name) if parent!=None else modvAdd(name).module()

    # add some inputs/outputs
    nD = m.iAdd('D')
    nCLK = m.iAdd('CLK')
    nQ = m.oAdd('Q')
    nQB = m.oAdd('QB')

    #let's create some modules ...
    mNOT0 = m.modAdd('NOT0',
        impl = 'local:/NOT'
        )
    mAND0 = m.modAdd('AND0',
        impl = 'local:/AND'
        )
    mAND1 = m.modAdd('AND1',
        impl = 'local:/AND'
        )
    mNOR0 = m.modAdd('NOR0',
        impl = 'local:/NOR'
        )
    mNOR1 = m.modAdd('NOR1',
        impl = 'local:/NOR'
        )
    ''' # cried off - not needed for q3sim ?
    mCRIED = m.modAdd('CRIED0',
        impl = 'local:/CRIED'
        )
    '''
    # ... and connect them
    nD.con(mNOT0.nod('A'))
    #nCLK.con(mCRIED.nod('A'))
    nD.con(mAND1.nod('A'))

    mNOT0.nod('Y').con(mAND0.nod('A'))
    #mCRIED.n('Y').c(mAND0.n('B'))
    #mCRIED.n('Y').c(mAND1.n('A'))
    nCLK.c(mAND0.n('B'))
    nCLK.c(mAND1.n('B'))

    mAND0.n('Y').c(mNOR0.n('A'))
    mAND1.n('Y').c(mNOR1.n('B'))

    mNOR0.n('Y').c(mNOR1.n('A'))
    mNOR1.n('Y').c(mNOR0.n('B'))

    #pin outputs ..
    mNOR0.n('Y').c(nQ)
    if nQB!=None: #QB not required
        mNOR1.n('Y').c(nQB)

    if m.isRoot(): #bother with presentation only for root module
        # put it all in nice places ...
        mNOT0.setPos(-250.0,-70.0)
        mAND0.setPos(-120.0,-70.0)
        mAND1.setPos(-120.0,90.0)
        mNOR0.setPos(80.0,-70.0)
        mNOR1.setPos(80.0,70.0)
    
    return m #return new module

if __name__ == '__main__':
    makeDLatch('cpu-D-latch')