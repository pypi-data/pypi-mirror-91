import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DBJSONS",
    version="1.0.2",
    author="Afiq",
    author_email="muhammad184276@gmail.com",
    description="dbjson is a module that can help you use json as database",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/IM-code111/dbjson-1.0.1",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)