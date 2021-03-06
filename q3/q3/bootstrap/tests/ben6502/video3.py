
# https://www.youtube.com/watch?v=oO8_2JJV0B4

# Ben's part 3 is about assembler
# Let's play ...

# import some functions written
import q3.bootstrap.tests.ben6502.videos as v

rompath = v.videoCompile('video3.s')
# and run setup from previous video
exec(open(v.fpath+'video2.py').read())

