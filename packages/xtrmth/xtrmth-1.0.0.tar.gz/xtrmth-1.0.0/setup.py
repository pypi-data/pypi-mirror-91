from setuptools import find_packages, setup

setup(
    name='xtrmth',
    packages=find_packages(include=['xtrmth']),      
    version='1.0.0',
    description='assorted math functions, to provide all of oyur math needs.',
    author='William Nelson',
    license='MIT',
    install_requires=['typing', 'decimal'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests'
)