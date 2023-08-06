import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dataconda", # Replace with your own username
    version="0.0.1",
    author="Vinayak Vikram",
    author_email="subram.sesh@gmail.com",
    description="A python library for data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ploppy-pigeon/DataConda",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)