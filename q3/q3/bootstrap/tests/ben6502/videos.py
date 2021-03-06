from q3.api import *

def video1(modv):
    #now we'll need 6502 module from chips
    m6502 = modv.modAdd('C6502',
        impl='Q3Chips:/c6502'
        )

    # add few inputs to the module (they will be seen as outputs socket as module is in detail "inside" view state)
    ti1 = modv.module().ioAdd('i1',ioType = IoType.INPUT)
    ti2 = modv.module().ioAdd('i2',ioType = IoType.INPUT)
    ti3 = modv.module().ioAdd('i3',ioType = IoType.INPUT)

    # now we'll get some socket/node handles ...
    pRDY = m6502.nod('RDY')
    pRESB = m6502.nod('RESB')
    pNMIB = m6502.nod('NMIB')
    pIRQB = m6502.nod('IRQB')
    pPHI = m6502.nod('PHI0I')

    # ... and connect the inputs to them
    ti1.con(pRDY)
    ti1.con(pIRQB)
    ti1.con(pNMIB)
    ti2.con(pRESB)
    #ti3.con(pPHI)

    # some view tweeking
    m6502.setPos(-110.0,-200.0)
    m6502.view().expand() #impl().expand()

    #this is no longer needed i think
    #def mountMonitorM(self,obj, mname, handler):
    #    mountMonitor(obj, mname, handler)

    # now create a clock to tick the CPU
    clock = modv.modAdd('Clock',
        impl='Q3Chips:/Clock'
        )

    # connect it ti timer slot
    clock.nod('Y').con(pPHI)

    # set position
    clock.setPos(-40.0,-290.0)

    # ... and interval
    mod('Clock').impl().setInterval(1000) 

    # put some signals to the net...
    ti1.intSignal().setValue(1)

    sig('i2').setValue(1) 

#modv = modvAdd('Videos')

#video1(modv)
# cd /src/makaronLab/externalTools && wget http://sun.hasenbraten.de/vasm/release/vasm.tar.gz
# tar -xvf vasm.tar.gz && cd vasm && make CPU=6502 SYNTAX=oldstyle
# cd /src/makaronLab/q3/q3/bootstrap/tests/ben6502/ && hexdump -C a.out
fpath = '/src/makaronLab/q3/q3/bootstrap/tests/ben6502/'
def videoCompile(vName:str): 
    vasmbin = '/src/makaronLab/externalTools/vasm/vasm6502_oldstyle'

    # compile the assembler code
    import subprocess
    subprocess.call([vasmbin, '-Fbin','-dotdir',vName],cwd=fpath)

    # set rom path
    rompath = fpath+'a.out' 
    return rompath