import setuptools
from distutils.core import setup
from setuptools import setup, find_packages



setup(
    name='SpecAnalysis-cader-Cademan051',
    version='1.5.4.2',
    packages=find_packages(),
    install_requires=[
          'numpy',
          'PyQt5',
          'pyqtgraph',
          'numpy',
          'matplotlib',
          'scipy',
          'rpy2',
      ],
    include_package_data=True,
    package_data={'':['*.txt'],
                  '':['*.dat'],
                  '':['*.png']},
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.txt').read(),
)