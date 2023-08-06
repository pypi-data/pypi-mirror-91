# -*- coding: utf-8 -*-
"""
documentation
"""

from setuptools import setup, find_packages

setup(
    name='pilyso_io_omero',
    version='0.0.1.dev1',
    description='pilyso - image reading library - omero reader',
    long_description='Python Image anaLYsis SOftware library',
    author='Christian Sachs',
    author_email='c.sachs@fz-juelich.de',
    url='https://github.com/modsim/pilyso-io-omero',
    packages=find_packages(),
    requires=['numpy'],
    license='GPL',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
    ]
)
