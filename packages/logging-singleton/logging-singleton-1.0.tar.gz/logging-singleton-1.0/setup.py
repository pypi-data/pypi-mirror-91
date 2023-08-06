from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name = "logging-singleton",
    version = "1.0",

    package_dir = {'': 'src'},
    packages = ['logging_service'],
    install_requires = ['nose2>=0.9.2'],     # For testing

    # metadata for upload to PyPI
    author = "Andreas Paepcke",
    author_email = "paepcke@cs.stanford.edu",
    description = "Simple logging service shared by all application modules",
    long_description_content_type = "text/markdown",
    long_description = long_description,
    license = "BSD",
    url = "https://github.com/paepcke/logging_singleton.git",   # project home page, if any
)
print("To run tests, type 'nose2'")

