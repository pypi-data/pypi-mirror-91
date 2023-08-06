
from setuptools import setup, find_packages

setup(
  name="dirdb",
  version="0.1.0",
  author="Frank S. Hestvik",
  author_email="tristesse@gmail.com",
  long_description=open('README.md', 'r').read(),
  long_description_content_type='text/markdown',
  url="https://gitlab.com/franksh/dirdb",
  packages=find_packages(),
  license='MIT',
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  python_requires='>=3.6',
  install_requires=['filelock'])
