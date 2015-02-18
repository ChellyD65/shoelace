from setuptools import setup

setup(name='shoelace',
      version='0.2',
      description='A python package for RNA sequence data and expression level analysis and utilities for querying the NCBI Gene Expression Omnibus (GEO) database',
      url='http://github.com/ChellyD65/shoelace',
      author='Marcello DiStasio',
      license='GNU GPL',
      packages=['shoelace'],
      setup_requires=["numpy"],
      install_requires=["numpy", "pyemd", "Bio", "matplotlib", "sklearn", "scipy"],
      dependency_links=["git+https://github.com/wmayner/pyemd@develop#egg=pyemd", "git+https://github.com/biopython/biopython"],
      zip_safe=False)
