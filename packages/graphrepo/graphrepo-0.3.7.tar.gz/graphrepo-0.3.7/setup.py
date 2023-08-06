# v0.3.7 released
from setuptools import setup, find_packages

with open('requirements.txt') as reqs_file:
    requirements = reqs_file.read().splitlines()

setup(name="graphrepo",
      version="0.3.7",
      description="A tool that maps a Github repo to Neo4j and Helps Mining the Repo in the DB",
      url="https://github.com/NullConvergence/GraphRepo",
      license='Apache License',
      python_requires='>=3.5',
      install_requires=requirements,
      packages=find_packages('.'),
      package_dir={'graphrepo': 'graphrepo'})

# python3 setup.py sdist bdist_wheel
# python3 -m twine upload dist/*
