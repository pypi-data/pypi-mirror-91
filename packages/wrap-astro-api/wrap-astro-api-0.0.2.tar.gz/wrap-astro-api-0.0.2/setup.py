# To SAVE to pypi. From directory where setup.py is located:
#   python3 setup.py sdist bdist_wheel
#   python3 -m twine upload dist/*
#
# To GET from pypi:
#   

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wrap-astro-api", 
    version="0.0.2",
    author="S. Pothier",
    author_email="pothier@noao.edu",
    description="Python wrapper for Astro Archive web API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
