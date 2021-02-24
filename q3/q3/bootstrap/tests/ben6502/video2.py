

#https://www.youtube.com/watch?v=yl8vPW5hydQ


#first created a function "video1" from what was made in previous part to easilly share the work
from q3.api import *
from q3.bootstrap.tests.ben6502.videos import video1 

modv = modvAdd('Ben\'s video2')

video1(modv)


# now looks like we have to prepare a AT28C256 simulator ...
# so created ModuleImplAT28C256

mAT28C256 = modv.modAdd(
    'AT28C256',
    impl = 'Q3Chips:/AT28C256'

)