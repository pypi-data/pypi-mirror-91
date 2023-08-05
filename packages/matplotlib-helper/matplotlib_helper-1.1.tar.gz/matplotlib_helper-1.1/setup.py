from setuptools import setup

setup(
   name='matplotlib_helper',
   version='1.01',
   description='Module for helping and plotting in matplotlib',
   author='Santosh Kumar Radha',
   author_email='srr70@case.edu',
   packages=['matplotlib_helper'],  #same as name
   install_requires=['colour', 'matplotlib'], #external packages as dependencies
   license="MIT",
)