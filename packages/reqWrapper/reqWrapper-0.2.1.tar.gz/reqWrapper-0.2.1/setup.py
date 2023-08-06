from setuptools import setup

setup(
    name='reqWrapper',
    version='0.2.1',
    packages=['reqWrapper'],
    url='https://github.com/box-archived/reqWrap',
    license='Apache License 2.0',
    author='box-archived',
    author_email='box.cassette@gmail.com',
    description='Wrapper of requests with retry options',
    install_requires=['requests>=2.*']
)
