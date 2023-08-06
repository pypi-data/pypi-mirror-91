from setuptools import setup, Extension

import unittest
def my_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='unittest_*.py')
    return test_suite

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open('README.rst') as f:
    readme = f.read()

setup(
    name='gait-profile-score',
    author='Michael Jeffryes',
    author_email='mike.jeffryes@hotmail.com',
    url='',
    version='1.0.0',
    description='Calculates Gait Profile Score',
    #packages=['gpscalc'],
    py_modules=["gpscalculator",],
    package_dir={'':'gpscalc'},
    setup_requires=['wheel'],
    classifiers=[
        #"License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    #test_suite='tests'
    install_requires=requirements,
    long_description=readme,
    long_description_content_type='text/markdown',
    #test_suite='setup.my_test_suite',
)

# python setupy.py sdist bdist_wheel
# twine upload dist/* --skip-existing
