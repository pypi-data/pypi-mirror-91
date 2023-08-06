import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="data-engineering-extract-metadata",
    version="1.3.1",
    author="Alec Johnson",
    author_email="alec.johnson@digital.justice.gov.uk",
    description="Extract metadata for data engineering pipelines",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/moj-analytical-services/data-engineering-extract-metadata",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6, <4.0",
)
