import dansk
import pathlib
from setuptools import setup


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
