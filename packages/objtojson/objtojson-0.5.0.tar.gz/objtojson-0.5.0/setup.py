import pathlib

from setuptools import setup

from objtojson import __version__

README = (pathlib.Path(__file__).parent / 'README.md').read_text()

setup(
    name='objtojson',
    packages=['objtojson'],
    version=__version__,
    description='Object to JSON serialization with none to minimal need for custom declarations',
    long_description=README,
    long_description_content_type='text/markdown',
    author='Joerg Schroeter',
    license='MIT',
    url="https://github.com/joergrs/object-to-json",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    tests_require=['pytest'],
    python_requires='>=3.6',
)
