import os
import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='Tunapy',
    version="1.1.2",
    author="Edward Mensah",
    description="Get notified with events in bdm",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/edwarddubi/Tunapy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Environment :: Web Environment",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data = True,
    python_requires='>=3.6',
    entry_points = {
        'console_scripts': [
            'Tunapy=tunapy.main:main',
        ],
    },
)