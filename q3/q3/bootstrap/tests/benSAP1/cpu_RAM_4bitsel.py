
from q3.api import *

from q3.bootstrap.tests.benSAP1.common import make74LS163A
from q3.bootstrap.tests.benSAP1.cpu_OE_8bit_ei import makeOE8bitEI
from q3.bootstrap.tests.benSAP1.cpu_RAM_1bitsel import makeRAM1BITSEL

def makeRAM4BITSEL(name:str,parent:Module=None):
    #make root if parent is None
    m = parent.modAdd(name) if parent!=None else modvAdd(name).module()

    i=0
    while i <4:
        m.iAdd(f'A{i}')
        m.oAdd(f'O{i}')
        m1bs = makeRAM1BITSEL(f'1bitsel{i}',m)
        if m.isRoot(): #bother with presentation only for root module
            m1bs.setPos(-20,-170+(120*i))
        i=i+1
    i=0
    while i <4: 
        m.iAdd(f'B{i}')
        m.n(f'A{i}').c(m.mod(f'1bitsel{i}').n('A'))
        m.n(f'B{i}').c(m.mod(f'1bitsel{i}').n('B'))
        m.mod(f'1bitsel{i}').n('O').c(m.n(f'O{i}'))
        i=i+1       
        
    m.iAdd('SEL')
    i=0
    while i <4: 
        m.n('SEL').c(m.mod(f'1bitsel{i}').n('SEL'))
        i=i+1 
    return m

if __name__ == '__main__':
    makeRAM4BITSEL('cpu-RAM-4bitsel') 