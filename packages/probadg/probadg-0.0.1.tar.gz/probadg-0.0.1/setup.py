from setuptools import setup
import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setup(name='probadg',
      version = '0.0.1',
      author = 'Alejandro Duenas Garcia',
      author_email = 'alejandro19971231@gmail.com',
      long_description = long_description,
      long_description_content_type = 'text/markdown',
      description = 'Binomial and Gaussian objects',
      url = "https://github.com/Alejandro-Duenas/probadg",
      packages = setuptools.find_packages(),
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
      python_requires='>=3.6',
      zip_safe = False)