from setuptools import find_packages, setup

setup(
    name='csvHandler',
    packages=find_packages(include=['csvHandler']),
    version='0.1.4',
    description='csv in memory paginator',
    author='own-backup',
    license='MIT',
    install_requires=['pandas'],
    tests_require=['pytest']
)
