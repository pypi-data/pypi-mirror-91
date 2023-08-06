import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="package_passgen",
    version="0.0.1",
    author="Chris",
    author_email="christopher.m9876@gmail.com",
    description="A package to generate strong random passwords",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chris1109873/package_passgen",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
