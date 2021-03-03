import os 

execF=execF
dirPath = os.path.dirname(os.path.realpath(__file__))


#outs = execF(dirPath+'/tests/test1.py')
outs = execF(dirPath+'/tests/test2.py')
#outs = execF(dirPath+'/tests/ben6502/video1.py')
#outs = execF(dirPath+'/tests/ben6502/video2.py')
#outs = execF(dirPath+'/tests/ben6502/video3.py')
#outs = execF(dirPath+'/tests/rs.py')
#outs = execF(dirPath+'/tests/74ls181.py')
print(outs)