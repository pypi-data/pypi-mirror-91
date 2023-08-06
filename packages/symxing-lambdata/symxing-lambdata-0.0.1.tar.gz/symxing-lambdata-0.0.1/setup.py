from setuptools import find_packages, setup 

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="symxing-lambdata",
    version="0.0.1",
    author="Symone Hohensee",
    author_email="symone.hohensee@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/symxing/lambdata-symxing",
    #keywords="",
    packages=find_packages() # ["my_lambdata"]
)