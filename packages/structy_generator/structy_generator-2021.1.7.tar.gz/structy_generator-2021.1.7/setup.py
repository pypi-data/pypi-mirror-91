#!/usr/bin/env python
# setup.py generated by flit for tools that don't yet use PEP 517

from distutils.core import setup

packages = \
['structy_generator', 'structy_generator.templates']

package_data = \
{'': ['*']}

install_requires = \
['jinja2']

entry_points = \
{'console_scripts': ['structy = structy_generator.__main__:main',
                     'structy_generator = structy_generator.__main__:main']}

setup(name='structy_generator',
      version='2021.1.7',
      description='Structy generator generates structy structs.',
      author='Alethea Katherine Flowers',
      author_email='thea@winterbloom.com',
      url='https://github.com/theacodes/structy',
      packages=packages,
      package_data=package_data,
      install_requires=install_requires,
      entry_points=entry_points,
     )
