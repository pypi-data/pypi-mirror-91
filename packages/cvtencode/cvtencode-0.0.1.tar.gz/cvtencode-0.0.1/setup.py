import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cvtencode",
    version="0.0.1",
    author="doupongzeng",
    author_email="huangzeng2016@126.com",
    description="tiny convert encode tool, just for convenience",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/doupongzeng/cvtencode",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)