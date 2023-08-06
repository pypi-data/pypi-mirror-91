import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="example-pkg-kriegersaurusrex", 
    version="1",
    author="Alex Krieger",
    author_email="kriegersaurusrex@gmail.com",
    description="Test package for DS22",
    long_description="Test package for DS22 Lambda School",
    long_description_content_type="text/markdown",
    url="https://github.com/kriegersaurusrex/lambdata-22",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)