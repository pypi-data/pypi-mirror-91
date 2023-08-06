import os
from setuptools import setup, find_packages


def read_file(filename):
    filepath = os.path.join(os.path.dirname(__file__), filename)
    return open(filepath, 'r').read()

setup(
    name='junebug',
    version='0.2.0',
    url='http://github.com/praekelt/junebug',
    license='BSD',
    description=(
        'A system for managing text messaging transports via a RESTful HTTP '
        'interface'),
    long_description=read_file('README.rst'),
    author='Praekelt Foundation',
    author_email='dev@praekeltfoundation.org',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        # We install pyasn1 first, because setuptools gets confused if it
        # installs pyasn1-modules first.
        'pyasn1',
        'klein<=17.10.0',
        'jsonschema',
        'treq<20.4.1',  # https://github.com/twisted/treq/issues/303
        'Twisted>=20.3.0,<21.0.0',
        'vumi>=0.6.19',
        'confmodel',
        'PyYAML',
        'raven>=6.0.0,<7.0.0',
    ],
    entry_points='''
    [console_scripts]
    jb = junebug.command_line:main
    ''',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP',
    ],
    zip_safe=False
)
