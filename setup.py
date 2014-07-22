from setuptools import setup, find_packages

setup(
    name="edx-jsme",
    version="1.0",
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        'XModule',
    ],
)
