#from setuptools import setup
from distutils.core import setup, Extension

#,"-lxi", "-lxrandr","-lglfw3","-lGLU", "-lGL", "-lGLEW""-lX11","-lasound","-z defs|--no-undefined"
#'xrandr', 'xi', 'xxf86vm', 'gl''glew', 'glfw3',"-shared","-DC6502OFF"
def main():
    setup(
        name='q3c',
        version='0.0.1',
        description='',
        long_description='',
        url='https://github.com/virtimus/makaronLab/q3/q3c',
        author='virtimus',
        author_email='virtimus@gmail.com',
        ext_modules=[
                Extension("q3c", ["q3cmodule.c","shared.c","cpc.c","wq6502.c"], 
                        extra_compile_args = ["-O0", "-pthread","-lX11","-lXi","-lXcursor"],
                        include_dirs = ['/src/makaronLab/externalTools/chips/chips','/src/makaronLab/libmakaron/include','/src/makaronLab/q3/q3c'],
                        libraries = ['GL','GLU','X11','asound','Xi','Xcursor'],
                        library_dirs = ['/usr/lib'],
                        #sources = []
                        )              
                ],    
        classifiers=['Development Status :: 1 - Planning'],
    )

if __name__ == "__main__":
    main()