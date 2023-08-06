# # from __future__ import absolute_import
# # from __future__ import unicode_literals
# # from os.path import dirname, abspath, join

# # from setuptools import setup, find_packages

# # try:
# #     with open('README.rst') as f:
# #         readme = f.read()
# # except IOError:
# #     readme = ''


# # def _requires_from_file(filename):
# #     return open(filename).read().splitlines()


# # package_name = 'iSATex'

# # here = dirname(abspath(__file__))
# # version = next((line.split('=')[1].strip().replace("'", '')
# #                 for line in open(join(here, package_name, '__init__.py'))
# #                 if line.startswith('__version__ = ')), '0.0.dev0')

# # setup(
# #     name=package_name,
# #     version=version,
# #     url='https://github.com/ryoTd0112/iSATex',
# #     author='RyoTandai',
# #     author_email='ryo.s1042@gmail.com',
# #     maintainer_email='ryo.s1042@gmail.com',
# #     description='GUI based software for bunch spectral data analysis',
# #     long_description='readme',
# #     packages=find_packages(),
# #     install_requires=_requires_from_file('requirements.txt'),
# #     license='MIT',
# #     classifiers=[
# #         'Programing Language :: Python :: 3.8',
# #         'Intended Audience :: Science/Research',
# #         'License :: OSI Approved :: MIT License',
# #     ],
# #     entry_points=f"""
# #     # -*- Entry points: -*-
# #     [console_scripts]
# #     iSATex = {package_name}.scripts.main : iSATex
# #     """
# # )

# import setuptools
# def _requires_from_file(filename):
#     return open(filename).read().splitlines()

# with open("README.md", "r", encoding="utf-8") as fh:
#     long_description = fh.read()
# print(setuptools.find_packages())
# setuptools.setup(
#     name="iSATex", # Replace with your own username
#     version="0.0.2",
#     author="RyoTandai",
#     author_email="ryo.s1042@gmail.com",
#     description="GUI based software for bunch spectral data analysis",
#     long_description=long_description,
#     long_description_content_type="text/markdown",
#     url="https://github.com/ryoTd0112/iSATex",
#     packages=setuptools.find_packages(),
#     classifiers=[
#         "Programming Language :: Python :: 3",
#         "License :: OSI Approved :: MIT License",
#         "Operating System :: OS Independent",
#     ],
#     install_requires=_requires_from_file('requirements.txt'),
#     python_requires='>=3',
# )

# # import setuptools

# # setuptools.setup()


# -*- coding: utf-8 -*-

from setuptools import setup
from codecs import open
from os import path
import re

package_name = "iSATex"

root_dir = path.abspath(path.dirname(__file__))

def _requirements():
    return [name.rstrip() for name in open(path.join(root_dir, 'requirements.txt')).readlines()]


def _test_requirements():
    return [name.rstrip() for name in open(path.join(root_dir, 'test-requirements.txt')).readlines()]

with open(path.join(root_dir, package_name, '__init__.py')) as f:
    init_text = f.read()
    version = re.search(r'__version__\s*=\s*[\'\"](.+?)[\'\"]', init_text).group(1)
    license = re.search(r'__license__\s*=\s*[\'\"](.+?)[\'\"]', init_text).group(1)
    author = re.search(r'__author__\s*=\s*[\'\"](.+?)[\'\"]', init_text).group(1)
    author_email = re.search(r'__author_email__\s*=\s*[\'\"](.+?)[\'\"]', init_text).group(1)
    url = re.search(r'__url__\s*=\s*[\'\"](.+?)[\'\"]', init_text).group(1)

assert version
assert license
assert author
assert author_email
assert url

with open('README.rst', encoding='utf-8') as f:
    long_description = f.read()


setup(
    name=package_name,
    packages=[package_name],

    version=version,

    license=license,

    install_requires=_requirements(),
    # tests_require=_test_requirements(),

    author=author,
    author_email=author_email,

    url=url,

    description='GUI based software for bunch spectral data analysis',
    long_description=long_description,
    keywords='Spectrum, GUI',

    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)