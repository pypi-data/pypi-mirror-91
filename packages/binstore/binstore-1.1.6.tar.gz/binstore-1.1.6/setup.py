import setuptools
from distutils.core import setup, Extension, DEBUG

sfc_module = Extension('binstore', sources = ['module_binstore.c'])
setup(name = 'binstore',
    packages = setuptools.find_packages(),
    version = '1.1.6',
    license = 'MIT',
    description = 'C extension to implement storage of objects based on value-based binning where binned value determines index into array where object is stored',
    long_description = 'C extension to implement storage of objects based on value-based vinning where binned value determines index into array where object is stored',
    author = 'John Herrema',
    author_email = 'jherrema@gmail.com',
    keywords = ['binning'],
    ext_modules = [sfc_module],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7']

      )
