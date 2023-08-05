#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from setuptools import setup


# Get version without importing, which avoids dependency issues
def get_version():
    with open('perfbench/version.py') as version_file:
        return re.search(r"""__version__\s+=\s+(['"])(?P<version>.+?)\1""",
                         version_file.read()).group('version')


def _long_description():
    with open('README.rst', 'r') as f:
        return f.read()


required=[
    'tqdm>=4.6.1',
    'Cerberus>=1.1',
    'plotly>=3.0.0',
    'notebook>=6.0',
    'ipywidgets>=7.2',
]


if __name__ == '__main__':
    setup(
        name='perfbench',
        version=get_version(),
        description='perfbench measures execution time of code snippets with Timeit and uses Plotly to visualize the results.',
        long_description=_long_description(),
        author='Hasenpfote',
        author_email='Hasenpfote36@gmail.com',
        url='https://github.com/Hasenpfote/perfbench',
        download_url='',
        packages = ['perfbench'],
        keywords=['benchmark', 'performance', 'plot', 'plotly'],
        classifiers=[
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Development Status :: 5 - Production/Stable',
            'Environment :: Other Environment',
            'Intended Audience :: Developers',
            'Topic :: Software Development',
            'Topic :: Utilities'
        ],
        python_requires='>=3.5',
        install_requires=required,
    )
