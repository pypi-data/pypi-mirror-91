# -*- coding: utf-8 -*-
import ast
import os
import re
import sys

from setuptools import find_packages, setup

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

# parse version from locust/__init__.py
_version_re = re.compile(r"__version__\s+=\s+(.*)")
_init_file = os.path.join(ROOT_PATH, "locust", "__init__.py")
with open(_init_file, "rb") as f:
    version = str(ast.literal_eval(_version_re.search(f.read().decode("utf-8")).group(1)))

setup(
    name='pacs_locustio',
    version=version,
    description="Website load testing framework",
    long_description="""pacs Locust is a python utility for doing easy, distributed load testing of a web site""",
    classifiers=[
        "Topic :: Software Development :: Testing :: Traffic Generation",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
    ],
    keywords='',
    author='Jonatan Heyman, Carl Bystrom, Joakim Hamrén, Hugo Heyman',
    author_email='',
    url='https://github.com/pacslab/pacs_locust',
    license='MIT',
    packages=find_packages(exclude=['examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    test_suite="locust.test",
    install_requires=[
        "gevent>=20.9.0",
        "flask>=1.1.2",
        "Werkzeug>=1.0.1",
        "requests>=2.9.1",
        "msgpack>=0.6.2",
        "pyzmq>=16.0.2",
        "geventhttpclient>=1.4.4",
        "ConfigArgParse>=1.0",
        "psutil>=5.6.7",
        "Flask-BasicAuth>=0.2.0",
    ],
    tests_require=[
        "cryptography",
        "mock",
        "pyquery",
    ],
    extras_require={
        ":sys_platform == 'win32'": ["pywin32"],
    },
    entry_points={
        'console_scripts': [
            'pacs_locust = locust.main:main',
        ]
    },
)
