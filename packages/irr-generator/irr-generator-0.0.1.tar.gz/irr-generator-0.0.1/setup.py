import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="irr-generator", 
    version="0.0.1",
    author="James Di Trapani",
    author_email="james@ditrapani.com.au",
    description="Generate IRR Route Objects at scale quickly and without error",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jamesditrapani/irr-generator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "Topic :: System :: Networking"
    ],
    python_requires='>=3.6',
)