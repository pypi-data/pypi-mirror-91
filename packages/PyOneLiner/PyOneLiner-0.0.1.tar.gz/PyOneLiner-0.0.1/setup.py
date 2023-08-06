from setuptools import setup, find_packages
import PyOneLiner

setup(
    name = 'PyOneLiner',
 
    version = PyOneLiner.__version__,
    packages = find_packages(),

    author = "Maurice Lambert", 
    author_email = "mauricelambert434@gmail.com",
 
    description = "This package implement a code OneLiner for python (write a script and get it in oneline).",
    long_description = open('README.md').read(),
    long_description_content_type="text/markdown",
 
    include_package_data = True,

    url = 'https://github.com/mauricelambert/PyOneLiner',
 
    classifiers = [
        "Programming Language :: Python",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8"
    ],
 
    entry_points = {
        'console_scripts': [
            'PyOneLiner = PyOneLiner:oneliner'
        ],
    },
    python_requires='>=3.6',
)