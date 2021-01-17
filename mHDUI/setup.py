from setuptools import setup, find_packages


def scm_version():
    def local_scheme(version):
        if version.tag and not version.distance:
            return version.format_with("")
        else:
            return version.format_choice("+{node}", "+{node}.dirty")
    return {
        #"relative_to": __file__,
        "version_scheme": "guess-next-dev",
        "local_scheme": local_scheme
    }


setup(
    name="mhdui",
    author="virtimus",
    author_email="virtimus@gmail.com",
    description="Python toolbox for digital hardware UI",
    python_requires="~=3.6",
    packages=find_packages()
)
