"""
Gremlinpy
------

Gremlinpy is a graph abstraction layer that converts Python objects
to Gremlin/Groovy strings.
"""
from setuptools import setup, find_packages

# get the version information
exec(open('gremlinpy/version.py').read())

setup(
    name = 'gremlinpy',
    packages = find_packages(),
    version = __version__,
    description = 'Python GAL for Gremlin/Groovy syntax',
    url = 'https://github.com/emehrkay/gremlinpy',
    author = 'Mark Henderson',
    author_email = 'emehrkay@gmail.com',
    long_description = __doc__,
    install_requires = [
        'six',
    ],
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2.7',
        'Environment :: Web Environment',
        'Topic :: Database',
        'Topic :: Database :: Front-Ends',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Distributed Computing',
        'Intended Audience :: Developers',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
        'Operating System :: MacOS :: MacOS X',
    ],
    test_suite = 'gremlinpy.tests',
)
