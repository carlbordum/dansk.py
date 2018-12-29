import dansk
import os
import pathlib
from setuptools import setup, find_packages


def get_site_packages_path():
    virtualenv = os.environ.get("VIRTUAL_ENV")
    if virtualenv:
        from distutils.sysconfig import get_python_lib
        return get_python_lib()
    import site
    return site.getusersitepackages()


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
    data_files=[(get_site_packages_path(), ["zzz_register_dansk_encoding.pth"])],
)
