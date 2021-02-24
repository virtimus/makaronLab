rom = bytearray([0xea]*32768)

with open('rom.bin','wb') as outFile:
    outFile.write(rom)