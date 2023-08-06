import setuptools
from pathlib import Path

setuptools.setup(
    name="leepdf",
    version=1.0,
    long_decription=Path("README.md").read_text(),
    package=setuptools.find_packages(exclude=["tests", "data"])
)