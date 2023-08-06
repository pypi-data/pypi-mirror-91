import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyLogicGates",
    version="0.0.1",
    author="B00bleTeA",
    author_email="asnojus039@gmail.com",
    description="use logic gates in python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/B00bleaTea/PyLogicGates",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)