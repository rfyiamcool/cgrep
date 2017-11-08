#!/usr/bin/env python

from setuptools import setup
import os
import os.path


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='cgrep',
    version='0.1',
    description='color grep',
    long_description=open('README.md').read(),
    keywords=["cgrep", "fengyun", "ruifengyun"],
    url='http://xiaorui.cc',
    author='ruifengyun',
    author_email='rfyiamcool@163.com',
    py_modules=['cgrep', 'termcolor'],
    license="MIT",
    entry_points={
        'console_scripts': [
            'cgrep = cgrep:main',
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.0',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
