#!/usr/bin/env python

from setuptools import find_packages, setup


setup(name='imgr',
      version='v0.0.1',
      description='Docker image manager',
      author='Liam Tengelis',
      author_email='liam@tengelisconsulting.com',
      url='https://github.com/tengelisconsulting/imgr',
      download_url=(""),
      packages=find_packages(),
      package_data={
          '': ['*.yaml'],
      },
)
