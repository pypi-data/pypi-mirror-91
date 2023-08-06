import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="odoogap-mtd",
    version="0.1.0",
    author="OdooGap",
    author_email="",
    description="MTD Library For OdooGAP",
    long_description="OdooGAP MTD external libray",
    long_description_content_type="text/markdown",
    url="https://github.com/odoogap/mtd_library",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
