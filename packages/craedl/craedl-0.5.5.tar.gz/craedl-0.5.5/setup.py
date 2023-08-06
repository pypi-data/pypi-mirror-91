# Copyright 2019 The Johns Hopkins University
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import setuptools

from craedl import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='craedl',
    version=__version__,
    author='Craedl.org',
    author_email='webmaster@craedl.org',
    description='A Python SDK for Craedl',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/craedl/craedl-sdk-python',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'python-dateutil',
        'requests',
    ],
    entry_points = {
        'console_scripts': [
            'craedl-token=craedl.__main__:main',
        ],
    },
)
