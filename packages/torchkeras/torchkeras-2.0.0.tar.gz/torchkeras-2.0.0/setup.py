# -*- coding:utf-8 -*-
import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="torchkeras",
    version="2.0.0",
    author="PythonAiRoad",
    author_email="lyhue1991@163.com",
    description="pytorch❤️ keras",
    long_description=long_description,
    install_requires=[           
         'pandas>=0.24.2',
         'pytorch_lightning>=1.1.4',
         'prettytable>=0.7.2'
         'tqdm>=4.31.1'
       ],
    long_description_content_type="text/markdown",
    url="https://github.com/lyhue1991/torchkeras",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5'
)

