# -*- coding: utf-8 -*-
"""
This module contains the tool of recensio.contenttypes

"""
import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '2.10.7.dev0'

long_description = (
    read('README.txt')
    + '\n' +
    'Requirements\n'
    '************\n'
    + '\n' +
    read('REQUIREMENTS.txt')
    + '\n' +
    'Change history\n'
    '**************\n'
    + '\n' +
    read('CHANGES.txt')
    + '\n' +
    'Detailed Documentation\n'
    '**********************\n'
    + '\n' +
    read('recensio', 'contenttypes', 'README.txt')
    + '\n' +
    'Contributors\n'
    '************\n'
    + '\n' +
    read('CONTRIBUTORS.txt')
    + '\n' +
    'Download\n'
    '********\n')

tests_require = ['zope.testing', 'mock']

setup(name='recensio.contenttypes',
      version=version,
      description="",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        'Framework :: Plone',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        ],
      keywords='',
      author='SYSLAB.COM',
      author_email='info@syslab.com',
      url='http://svn.plone.org/svn/collective/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['recensio', ],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        'Plone',
                        'swiss',
                        'xlrd',
                        'html5lib',
                        'pyPdf',
                        'reportlab',
                        ],
      tests_require=tests_require,
      extras_require=dict(test=tests_require),
      test_suite='recensio.contenttypes.tests.test_docs.test_suite',
      entry_points="""
      # -*- entry_points -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      setup_requires=["PasteScript"],
      paster_plugins=["ZopeSkel"],
      )
