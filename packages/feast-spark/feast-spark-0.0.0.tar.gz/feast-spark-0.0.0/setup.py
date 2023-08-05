from distutils.core import setup

# setup(
#     name='Feast Spark',
#     version='0.1dev',
#     packages=['towelstuff',],
#     license='Creative Commons Attribution-Noncommercial-Share Alike license',
#     long_description=open('README.txt').read(),
# )

# from setuptools import  setup

NAME = "feast-spark"
DESCRIPTION = "Python Spark SDK for Feast"
URL = "https://github.com/feast-dev/feast-spark"
AUTHOR = "Feast Developers"
REQUIRES_PYTHON = ">=3.6.0"

setup(
    name=NAME,
    author=AUTHOR,
    description=DESCRIPTION,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    # packages=['feast-spark',], 
    license="Apache"
)