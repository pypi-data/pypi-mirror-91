from setuptools import setup

setup(
   name='matplotlib_helper',
   version='1.0',
   description='Module for helping and plotting in matplotlib',
   author='Santosh Kumar Radha',
   author_email='srr70@case.edu',
   packages=['matplotlib_helper'],  #same as name
   install_requires=['colors', 'matplotlib'], #external packages as dependencies
)