import dansk
import os
import pathlib
from setuptools import setup, find_packages


# Here's a glorious hack;
#   `dansk` has to be imported on startup before the `# coding=dansk`
#   line has been read. site.py runs all .pth files in site-packages if
#   the first word is import. Yeah.
#   Stolen from Ned Batchelder
def get_site_packages_path():
    virtualenv = os.environ.get("VIRTUAL_ENV")
    if virtualenv:
        from distutils.sysconfig import get_python_lib
        return get_python_lib()
    import site
    return site.getusersitepackages()

site_packages = pathlib.Path(get_site_packages_path())
# filename starts with zzz because they are run alphabetically and
# `dansk` has to be on path before it is imported.
dansk_pth = site_packages / "zzz_register_dansk_encoding.pth"
with open(dansk_pth, "w+") as f:
    f.write("import dansk")

this_dir = pathlib.Path(__file__).parent.absolute()
with open(this_dir / "README.rst", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="dansk",
    version=dansk.__version__,
    license="MIT",
    url="https://github.com/carlbordum/dansk.py",
    author="Carl Bordum Hansen",
    author_email="carl@bordum.dk",
    description="Python, but danish.",
    long_description=long_description,
    platforms="any",
    py_modules=["dansk"],
)
