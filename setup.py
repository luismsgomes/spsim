from setuptools import setup, find_packages
from os import path
import re


def packagefile(*relpath):
    return path.join(path.dirname(__file__), *relpath)


def read(*relpath):
    with open(packagefile(*relpath)) as f:
        return f.read()


def get_version(*relpath):
    match = re.search(
        r'''^__version__ = ['"]([^'"]*)['"]''',
        read(*relpath),
        re.M
    )
    if not match:
        raise RuntimeError('Unable to find version string.')
    return match.group(1)


setup(
    name='spsim',
    version=get_version('src', 'spsim', '__init__.py'),
    description='A spelling similarity measure for cognate identification.',
    long_description=read('README.rst'),
    url='https://github.com/luismsgomes/spsim',
    author='Luís Gomes',
    author_email='luismsgomes@gmail.com',
    license='MIT',
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Topic :: Text Processing :: Linguistic',
    ],
    keywords='text bilingual cognate mt machine translation',
    setup_requires=[
        'pytest',
        'coverage',
        'pytest-cov',
    ],
    install_requires=[
        'munkres',
        'stringology',
    ],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': [
            'spsim=spsim.__main__:main',
        ],
    },
)
