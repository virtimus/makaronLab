import os 

execF=execF
dirPath = os.path.dirname(os.path.realpath(__file__))

#outs = execF(dirPath+'/tests/test1.py')
#outs = execF(dirPath+'/tests/test2.py')
#outs = execF(dirPath+'/tests/ben6502/video1.py')
#outs = execF(dirPath+'/tests/ben6502/video2.py')
#outs = execF(dirPath+'/tests/ben6502/video3.py')
##outs = execF(dirPath+'/tests/rs.py')
#outs = execF(dirPath+'/tests/74ls181.py')
#outs = execF(dirPath+'/tests/ben6502/video7.py')
#outs = execF(dirPath+'/tests/ben6502/video5.py')

# building Bens 8bit SAP1
#outs = execF(dirPath+'/tests/benSAP1/cpu_D_latch.py', asMain=True)
#outs = execF(dirPath+'/tests/benSAP1/cpu_D_latch_1bitreg.py', asMain=True)
outs = execF(dirPath+'/tests/benSAP1/cpu_D_latch_8bitreg.py', asMain=True)


print(outs)