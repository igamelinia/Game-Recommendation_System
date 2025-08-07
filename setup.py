from setuptools import setup, find_packages 

with open("requirements.txt") as f:
    requirement = f.read().splitlines()

setup(
    name="Game-Recommendation-System",
    version="1.0",
    author="Iga Melinia",
    packages=find_packages(),
    install_requires = requirement
)