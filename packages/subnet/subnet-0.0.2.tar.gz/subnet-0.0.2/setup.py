import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="subnet",
    version="0.0.2",
    author="Usama Imdad",
    author_email="usamaimdadsian@gmail.com",
    description="A package to subnet ip address for static or dynamic networking.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/usamaimdadsian/subnet-pkg",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)