from setuptools import setup


AUTHOR='Omar Elazhary'
AUTHOR_EMAIL='omazhary@gmail.com'
LICENSE='MIT'
SHORT_DESCRIPTION='RepoSherlock facilitates data retrieval from some repository management services.'
VERSION='0.1.0'
URL=''

with open("README.rst", "r", encoding="utf-8") as long_description_in:
    long_description = long_description_in.read()

setup(
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    name='reposherlock',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    description=SHORT_DESCRIPTION,
    install_requires=['bs4'],
    keywords='research mining repository scraper',
    license='MIT',
    long_description=long_description,
    packages=['reposherlock'],
    python_requires='>=3.6',
    url='https://reposherlock.readthedocs.io/en/latest/index.html',
    version=VERSION,
    zip_safe=False
)