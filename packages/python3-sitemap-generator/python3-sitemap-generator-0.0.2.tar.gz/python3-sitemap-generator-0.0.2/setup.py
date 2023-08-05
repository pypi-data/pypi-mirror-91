import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python3-sitemap-generator", # Replace with your own username
    version="0.0.2",
    author="Various",
    author_email="kontakt@stefan-hesse.net",
    description="Python3 port of python-sitemap-generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/reinoldus/python3-sitemap-generator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)