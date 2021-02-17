from distutils.core import setup, Extension

#,"-lxi", "-lxrandr","-lglfw3","-lGLU", "-lGL", "-lGLEW""-lX11","-lasound","-z defs|--no-undefined"
#'xrandr', 'xi', 'xxf86vm', 'gl''glew', 'glfw3',"-shared",
def main():
    setup(
       name="wqc",
       version="1.0.0",
       description="WQC development package.",
       author="mb",
       author_email="virtimus@gmail.com",
       ext_modules=[
              Extension("wqc", ["wqcmodule.c","wq6502.c","cpc.c"], 
                     extra_compile_args = ["-O0", "-pthread","-lX11","-lXi","-lXcursor"],
                     include_dirs = ['/src/makaronLab/externalTools/chips/chips','/src/makaronLab/libmakaron/include','/src/makaronLab/wq/wqc'],
                     libraries = ['GL','GLU','X11','asound','Xi','Xcursor'],
                     library_dirs = ['/usr/lib'],
                     #sources = []
                     )              
              ],
       )


if __name__ == "__main__":
    main()
