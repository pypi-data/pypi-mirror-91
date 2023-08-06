import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
  name = 'XperiBot',
  packages = ['xperibot'],
  version = '0.1.0',
  description = 'A telegram bot to track ML experiments',
  long_description = 'A telegram bot to track ML experiments',
  author = 'Marco Formoso',
  author_email = 'marco.a.formoso@gmail.com',
  url = 'https://github.com/Skalextric/XperiBot',
  keywords = ['telegram', 'bot', 'machine learning', 'experiments'], 
  classifiers = [
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.9",
    ],
  install_requires = ['python-telegram-bot', 'matplotlib'],
  license="Apache 2.0",
)