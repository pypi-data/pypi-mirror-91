import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(name = 'outliers-detection',
      version = '0.12',
      long_description=README,
      description = 'Outlier Detection',
      packages = ['EdaFirstPhase'],
      zip_safe = False,
      author = 'Gaurav Srivastava',
      author_email='gaurav0535@hotmail.com',
      license='MIT'
      )

