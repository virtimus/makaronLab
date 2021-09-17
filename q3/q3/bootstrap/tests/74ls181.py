from q3.api import *

fpath = '/src/makaronLab/q3/q3/bootstrap/tests/'
path74LS181= fpath+'74181.v'
import os.path
if not os.path.isfile(path74LS181):
    # load veriilog
    import subprocess
    subprocess.call(['wget', 'http://web.eecs.umich.edu/~jhayes/iscas.restore/74181.v'],cwd=fpath)




#@refs:https://github.com/PyHDI/Pyverilog/blob/develop/examples/example_parser.py

import pyverilog
from pyverilog.vparser.parser import parse
import sys
import os
from optparse import OptionParser


def loadVerilog(file:str):
    INFO = "Verilog code parser"
    VERSION = pyverilog.__version__
    USAGE = "Usage: python example_parser.py file ..."

    def showVersion():
        print(INFO)
        print(VERSION)
        print(USAGE)
        sys.exit()
    '''
    optparser = OptionParser()
    optparser.add_option("-v", "--version", action="store_true", dest="showversion",
                         default=False, help="Show the version")
    optparser.add_option("-I", "--include", dest="include", action="append",
                         default=[], help="Include path")
    optparser.add_option("-D", dest="define", action="append",
                         default=[], help="Macro Definition")
    (options, args) = optparser.parse_args()
    '''
    '''
    filelist = args
    if options.showversion:
        showVersion()

    for f in filelist:
        if not os.path.exists(f):
            raise IOError("file not found: " + f)

    if len(filelist) == 0:
        showVersion()
    '''
    filelist = [file]

    print('dupa')

    ast, directives = parse(filelist)
                            #preprocess_include=options.include,
                            #preprocess_define=options.define)

    #print(ast.show())
    #for lineno, directive in directives:
        #print('Line %d : %s' % (lineno, directive))
    indent = 1
    def show(self, buf = sys.stdout, offset=0, attrnames=False, showlineno=True):
        
        lead = f'[{offset}] ' 

        buf.write(lead + self.__class__.__name__ + ': ')

        if self.attr_names:
            if attrnames:
                nvlist = [(n, getattr(self, n)) for n in self.attr_names]
                attrstr = ', '.join('%s=%s' % (n, v) for (n, v) in nvlist)
            else:
                vlist = [getattr(self, n) for n in self.attr_names]
                attrstr = ', '.join('%s' % v for v in vlist)
            buf.write(attrstr)

        if showlineno:
            buf.write(' (at %s)' % self.lineno)

        buf.write('\n')

        for c in self.children():
            show(c, buf, offset + indent, attrnames, showlineno)

    def loadModules(astObj, mDict, buf = sys.stdout, offset=0, attrnames=False, showlineno=True):

        oName = astObj.__class__.__name__
        if oName == 'ModuleDef':
            mDict[astObj.name] = astObj
        if offset == 2:
            buf.write(f'[loadModules] {astObj.__class__.__name__} \n')

        for c in astObj.children():
            loadModules(c, mDict, buf, offset + indent, attrnames, showlineno)

    def loadPortArg(ast,mDict,parent):
        print(f'loading portArg:{ast.name}')

    def loadPortArgs(ast,mDict,parent):
        cName = ast.__class__.__name__ 
        if cName == 'Identifier':
            ind = len(mDict['_ports'])
            mDict['_ports'][ind]={}
            mDict['_ports'][ind]['ident']=ast.name
            mDict['_ports'][ind]['identWInd']=ast.name
        if cName == 'IntConst':
            ind = len(mDict['_ports'])-1
            mDict['_ports'][ind]['index']=ast.value
            mDict['_ports'][ind]['identWInd']+=f'[{ast.value}]'


             
        for c in ast.children():
            loadPortArgs(c,mDict,parent)        

    def loadInstance(ast,mDict,parent):
        print(f'loading instance:{ast.name} module:{ast.module}')
        result = None
        tmodule = ast.module
        tname = ast.name
        if tmodule in ['xor','or','and','not','nand','nor']:

            if tname == 'CN4bgate':
                print('debher')    
            pPorts = mDict['_ports']
            mDict['_ports']={}
            loadPortArgs(ast,mDict,parent)
            lp = len(mDict['_ports'])
            if lp >3: #multiport version
                gname = su.toUpper(tmodule)+'4'
            else: #2inp
                gname = su.toUpper(tmodule)
            

            gate = parent.modAdd(tname,
                impl = f'local:/{gname}'
                )

            for k in mDict['_ports']:
                dv = mDict['_ports'][k]
                dvWind = dv['identWInd']
                if k==0: #output
                    mDict['_outputs'][dvWind]=gate.nod('Y')
                else:
                    aa = ord('A')
                    ii = k-1
                    cg = chr(aa+ii)
                    tn = gate.nod(cg)
                    mDict['_inputs'][dvWind]=tn
                    if dvWind in mDict['_outputs']:
                        sn = mDict['_outputs'][dvWind]
                        if tn == None:
                            print('got a prob')
                        sn.connect(tn)
            #for k in 
            mDict['_ports'] = pPorts
        elif tmodule in ['buf']:
            pPorts = mDict['_ports']
            mDict['_ports']={}
            loadPortArgs(ast,mDict,parent)
            lp = len(mDict['_ports'])
            if lp == 2:
                for k in mDict['_ports']:
                    dv = mDict['_ports'][k]
                    dvIdent = dv['ident']
                    dvWind = dv['identWInd']
                    if k==0: #output
                        sName = dvIdent
                    else: #input
                        sIdent = dvIdent
                        sIdentWI = dvWind
                        sIndex = dv['index']
                mMap = parent.mod('sigMap'+sIdent)
                nO=mMap.ioAdd(sName,
                    ioType = IoType.OUTPUT
                    )
                mMap.setSigFormula(sName,f'=IS[{sIndex}]')
                mDict['_outputs'][sName]=nO
            else:
                assert False, f'[loadInstance] Unhandled ports number for buffer:{lp}'

            mDict['_ports'] = pPorts
        elif tmodule in mDict: #module
            mt = parent.modAdd(tname)
            pInps = mDict['_inputs']
            pOuts = mDict['_outputs']
            pOutsF = mDict['_outputsF']
            loadModule(mDict[tmodule],mDict,mt)
            mDict['_inputs'] = pInps
            mDict['_outputs'] = pOuts
            mDict['_outputsF'] = pOutsF
            for n in mt.nodes().values():
                if n.ioType() in [IoType.INPUT,IoType.DYNAMIC]:
                    mDict['_inputs'][n.name()]=n
                if n.ioType() in [IoType.OUTPUT,IoType.DYNAMIC]:
                    mDict['_outputs'][n.name()]=n
                pass
        else:
            assert False, f'[loadInstance] Unhandled module name:{tmodule}'
        return result
        

    def loadInstances(ast,mDict,parent):
        cName = ast.__class__.__name__ 
        if cName == 'Instance':
            loadInstance(ast,mDict,parent)
             
        for c in ast.children():
            loadInstances(c,mDict,parent)

    def loadOutputs(ast,mDict,parent):
        cName = ast.__class__.__name__
        if cName == 'Decl':
            ind = len(mDict['_outputsF'])-1
            if ind>-1: 
                mDict['_outputsF'][ind]['ended']=True

        if cName == 'Output':
            ind = len(mDict['_outputsF'])
            mDict['_outputsF'][ind]={}
            mDict['_outputsF'][ind]['ended']=False
            mDict['_outputsF'][ind]['name']=ast.name

        if cName == 'IntConst':
            ind = len(mDict['_outputsF'])-1
            if ind>-1 and not mDict['_outputsF'][ind]['ended']:
                if 'from' not in mDict['_outputsF'][ind]:
                    mDict['_outputsF'][ind]['from'] = ast.value
                else:
                    mDict['_outputsF'][ind]['to'] = ast.value

        for c in ast.children():
            loadOutputs(c,mDict,parent) 


    def loadInputs(ast,mDict,parent):
        cName = ast.__class__.__name__ 
        
        if cName == 'Decl':
            ind = len(mDict['_inputs'])-1
            if ind>-1: 
                mDict['_inputs'][ind]['ended']=True
        if cName == 'Input':
            ind = len(mDict['_inputs'])
            mDict['_inputs'][ind]={}
            mDict['_inputs'][ind]['ended']=False
            mDict['_inputs'][ind]['name']=ast.name

        if cName == 'IntConst':
            ind = len(mDict['_inputs'])-1
            if ind>-1 and not mDict['_inputs'][ind]['ended']:
                if 'from' not in mDict['_inputs'][ind]:
                    mDict['_inputs'][ind]['from'] = ast.value
                else:
                    mDict['_inputs'][ind]['to'] = ast.value

        for c in ast.children():
            loadInputs(c,mDict,parent)

    def processOutputs(mDict,parent):
        for k in mDict['_outputsF']:
            idef = mDict['_outputsF'][k]
            nOutName = idef['name']
            if nOutName == 'CN4b':
                print('trace') 
            if 'from' in idef and idef['from']!='0':
                sz = int(idef['from'])-int(idef['to'])+1
                nOut = parent.ioAdd(nOutName,
                    ioType = IoType.OUTPUT,
                    size = sz
                    )
                mDict['_outputs'][nOutName]=nOut
                mapMod = parent.modAdd('sigMap'+nOutName)
                os1 = mapMod.ioAdd('OS',ioType=IoType.OUTPUT,size=sz)
                os1.connect(nOut)
                sformula ='=0'
                for i in range(0,sz,1):
                    nN = nOutName+f'{i}'
                    nNO = nOutName+f'[{i}]'
                    nn0 = mapMod.ioAdd(nN,
                        ioType = IoType.INPUT
                        )
                    if nNO == 'F[0]':
                        print('trace')
                    if nNO in mDict['_outputs']:
                        ns = mDict['_outputs'][nNO]
                        ns.connect(nn0)
                    else: # not mapped ? or defined as from to without
                        pass
                    #mapMod.setSigFormula(nN,f'= OS[{i}]')
                    #mDict['_outputs'][nN]=nn0
                    sformula += f'+({nN}.value()<<{i})'
                mapMod.setSigFormula('OS',sformula)
            else:
                nOut = parent.ioAdd(nOutName,
                    ioType = IoType.OUTPUT
                    )
                if nOutName in mDict['_outputs']:
                    ns = mDict['_outputs'][nOutName]
                    ns.connect(nOut)
                else: #not used?
                    pass

    def processInputs(mDict,parent):
        for k in mDict['_inputs']:
            idef = mDict['_inputs'][k]
            nInpName = idef['name']
            if 'from' in idef:
                sz = int(idef['from'])-int(idef['to'])+1
                nInp = parent.ioAdd(nInpName,
                    ioType = IoType.INPUT,
                    size = sz
                    )
                mDict['_outputs'][nInpName]=nInp
                mapMod = parent.modAdd('sigMap'+nInpName)
                is1 = mapMod.ioAdd('IS',ioType=IoType.INPUT,size=sz)
                nInp.connect(is1)
                for i in range(0,sz,1):
                    nN = nInpName+f'[{i}]'
                    nn0 = mapMod.ioAdd(nN,
                        ioType = IoType.OUTPUT
                        )
                    mapMod.setSigFormula(nN,f'= IS[{i}]')
                    mDict['_outputs'][nN]=nn0
            else:
                nInp = parent.ioAdd(nInpName,
                    ioType = IoType.INPUT
                    )
                mDict['_outputs'][nInpName]=nInp

    def loadModule(astMod, mDict,parent):
        print(f'loading module {astMod.name}')
        mDict['_inputs']={}
        mDict['_outputs']={}
        loadInputs(astMod,mDict,parent)
        # now we'll build temporary graph modules for input singnal mapping
        processInputs(mDict,parent)        

        #mc = parent.modAdd(astMod.name)
        loadInstances(astMod,mDict,parent)
        mDict['_outputsF']={}
        loadOutputs(astMod,mDict,parent)
        processOutputs(mDict,parent)

        #show(astMod,attrnames=True)



    show(ast)
    mDict = {}
    loadModules(ast, mDict)
    print('dir(mDict.keys()):')
    for k in mDict:
        print(f'K:{k}')

    parentv = modvAdd('Summodule')
    parent = parentv.module()
    k = 'Summodule'
    mDict['_ports']=None
    #mDict['_sigs']=None
    loadModule(mDict[k],mDict,parent)

    parentv = modvAdd('CLAmodule')
    parent = parentv.module()
    k= 'CLAmodule'
    mDict['_ports']=None
    loadModule(mDict[k],mDict,parent)

    parentv = modvAdd('Dmodule')
    parent = parentv.module()
    k= 'Dmodule'
    mDict['_ports']=None
    loadModule(mDict[k],mDict,parent)

    parentv = modvAdd('Emodule')
    parent = parentv.module()
    k= 'Emodule'
    mDict['_ports']=None
    loadModule(mDict[k],mDict,parent)

    parentv = modvAdd('TopLevel74181')
    parent = parentv.module()
    k= 'TopLevel74181'
    mDict['_ports']=None
    loadModule(mDict[k],mDict,parent)

loadVerilog(path74LS181)