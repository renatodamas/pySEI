import os
import re
from setuptools import setup
#from pipenv import find_install_requires


def get_version(pkg_name, version_file='__version__.py'):
    here = os.path.abspath(os.path.dirname(__file__))
    version_file = os.path.join(here, pkg_name, version_file)
    version = open(version_file).read()
    version = re.search('[0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,2}', version).group()
    return version


pkg_name = 'pysei'
pkg_version = get_version(pkg_name)
pkgs = ['pysei']
install_requires = ['bs4', 'requests', 'lxml']  # find_install_requires()

config = dict(
    name=pkg_name,
    version=pkg_version,
    author='Rafael Alves Ribeiro',
    author_email='rafael.alves.ribeiro@gmail.com',
    url='https://github.com/renatodamas/pySEI.git',
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.8.6',
    ],
    packages=pkgs,
    license='License :: OSI Approved :: MIT License',
    install_requires=install_requires,
    setup_requires=['pytest-runner'],
    tests_require=[
        'pytest', 'pytest-cov', 'requests',
    ],
)

setup(**config)
