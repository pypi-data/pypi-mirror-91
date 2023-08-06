import setuptools
from distutils.core import setup

setup(
    name='SpecAnalysis-cader-Cademan051',
    version='1.4',
    packages=['Spec',],
    install_requires=[
          'numpy',
          'PyQt5',
          'pyqtgraph',
          'numpy',
          'matplotlib',
          'scipy',
          'rpy2',
      ],
    setup_requires=['setuptools_scm'],
    include_package_data=True,
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.txt').read(),
)