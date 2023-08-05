import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="betterjsonfs",
    version="0.1.2",
    author="Kool Author",
    author_email="besimat444@sofiarae.com",
    description="A horrible Idea",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bit.ly/betterjsonfs",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)