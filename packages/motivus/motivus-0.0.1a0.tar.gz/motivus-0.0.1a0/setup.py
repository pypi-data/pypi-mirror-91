import pathlib
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


# This call to setup() does all the work
setuptools.setup(
    name="motivus",
    version="0.0.1a",
    description="Motivus library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://motivus.cl",
    author="Motivus SpA",
    author_email="info@motivus.cl",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    packages=setuptools.find_packages(),
    install_requires=["websockets", "asyncio"],
    include_package_data=True,
    python_requires='>=3.6',
)
