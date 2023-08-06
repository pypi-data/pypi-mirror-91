import setuptools
from distutils.core import setup
from distutils.command.install import INSTALL_SCHEMES


for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']

setup(
    name='SpecAnalysis-cader-Cademan051',
    version='1.5',
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
    data_files=[('', ['LICENSE.txt'])],
    include_package_data=True,
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.txt').read(),
)