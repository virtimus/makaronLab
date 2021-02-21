import re
import sys, os
from streamlit.cli import main

if __name__ == '__main__':
    #tdir = os.path.dirname(sys.argv[0])
    #os.chdir(tdir)
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])   
    sys.exit(main())