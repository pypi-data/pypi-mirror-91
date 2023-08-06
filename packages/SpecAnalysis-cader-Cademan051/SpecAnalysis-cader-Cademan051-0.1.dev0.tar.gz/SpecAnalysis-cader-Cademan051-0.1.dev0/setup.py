import setuptools
from distutils.core import setup

setup(
    name='SpecAnalysis-cader-Cademan051',
    version='0.1dev',
    packages=['Spec',],
    install_requires=[
          'numpy',
          'PyQt5',
          'pyqtgraph',
          'numpy',
          'matplotlib.pyplot',
          'scipy',
          'rpy2',
      ],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.txt').read(),
)