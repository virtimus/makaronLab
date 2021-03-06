from q3.api import *

import q3.bootstrap.tests.ben6502.videos as v

rompath = v.videoCompile('video5.s')

execF(v.fpath+'video2.py')