from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pylint-testcode-plugin',
    version='0.0.2',
    url='https://github.com/Ewald91/pylint-testcode-plugin',
    author="Ewald Verhoeven",
    author_email="ewald@testcoders.nl",
    description='This plugin assists in writing high-quality testcode',
    py_modules=["pylint-testcode"],
    package_dir={'':'pylint_testcode'},
    classifiers=["Programming Language :: Python :: 3",
                "Programming Language :: Python :: 3.6",
                "Programming Language :: Python :: 3.7",
                "License :: OSI Approved :: GNU General Public License (GPL)",
                "Topic :: Software Development :: Testing",
                "Topic :: Software Development :: Testing :: Unit",
                "Topic :: Software Development :: Quality Assurance"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires= [
        "pylint ~=2.6.0"
    ]
)