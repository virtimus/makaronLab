
# https://www.youtube.com/watch?v=oO8_2JJV0B4

# Ben's part 3 is about assembler
# Let's play ...

# cd /src/makaronLab/externalTools && wget http://sun.hasenbraten.de/vasm/release/vasm.tar.gz
# tar -xvf vasm.tar.gz && cd vasm && make CPU=6502 SYNTAX=oldstyle
# cd /src/makaronLab/q3/q3/bootstrap/tests/ben6502/ && hexdump -C a.out
fpath = '/src/makaronLab/q3/q3/bootstrap/tests/ben6502/'
vasmbin = '/src/makaronLab/externalTools/vasm/vasm6502_oldstyle'

# compile the assembler code
import subprocess
subprocess.call([vasmbin, '-Fbin','-dotdir','video3.s'],cwd=fpath)

# set rom path
rompath = fpath+'a.out' 

# and run setup from previous video
exec(open(fpath+'video2.py').read())

