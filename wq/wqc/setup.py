from distutils.core import setup, Extension


def main():
    setup(
       name="wqc",
       version="1.0.0",
       description="WQC development package.",
       author="mb",
       author_email="virtimus@gmail.com",
       ext_modules=[
              Extension("wqc", ["wqcmodule.c","wq6502.c"], 
                     extra_compile_args = ["-O0", "-pthread"],
                     include_dirs = ['/src/makaronLab/externalTools/chips/chips'],
                     #libraries = ['tcl83'],
                     #library_dirs = ['/usr/local/lib'],
                     #sources = []
                     )              
              ],
       )


if __name__ == "__main__":
    main()
