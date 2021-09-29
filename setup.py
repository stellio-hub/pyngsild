from setuptools import setup, find_packages


setup(
    name="pyngsild",
    version="0.6.0",
    packages=find_packages(),
    install_requires=[
        'pytest==6.2.4',
        'pytz==2021.1',
        'tzlocal==2.1',
        'pytest-mock-server==0.2.0',
        'requests==2.25.1',
    ],
)
