
# returns a set of bits from 'pins' defined by start index(0-bases) of 'fr' and size of 'sz'
def readBits(pins,fr,sz):
    b = bin(pins)
    ones = pow(2, sz)-1
    ones_sh = ones << fr
    pins = pins & ones_sh
    pins = pins >> fr
    return pins

# takes first (little-endian) 'sz' bits from uint and puts them into pins at 'fr' and returns pins as result
def writeBits(pins,fr,sz,uint):
    #b = bin(pins)[::-1]
    #b = bin(uint)[::-1]
    ones = pow(2, sz)-1
    #b = bin(ones)[::-1]
    ones_sh = ones << fr
    #b = bin(ones_sh)[::-1]
    cuint = uint & ones
    #b=bin(cuint)[::-1]
    cuint = cuint << fr
    #b=bin(cuint)[::-1]
    pins = pins & ~ones_sh
    #b=bin(pins)[::-1]
    pins = pins | cuint
    #b=bin(pins)[::-1]
    return pins

def binlend(s):
    return bin(s)[::-1]