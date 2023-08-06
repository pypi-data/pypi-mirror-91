from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

with open("requirements.txt", "r") as f:
    requires = f.read().splitlines()

setup(name="stripcodecheats",
version="1.3",
author="Sachin Raja",
author_email="sachinraja2349@gmail.com",
license="MIT",
description="Cheats for the game StripCode by benawad utilizing the selenium library.",
long_description=long_description,
long_description_content_type="text/markdown",
url="https://github.com/xCloudzx/stripcodecheats",
packages=find_packages(),
install_requires=requires,
include_package_data=True,
classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
]
)