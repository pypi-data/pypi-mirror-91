from setuptools import setup, find_packages

README = 'zip entire directories recursively'

requires = []
tests_require = []

setup(name='zip-dir',
      version='1.0.0',
      description=README,
      long_description=README,
      url='https://github.com/wangyx01/zip-dir',
      classifiers=[
          "Programming Language :: Python",
      ],
      author='Yunxiang Wang',
      keywords='zip',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      extras_require={
          'testing': tests_require,
      },
      install_requires=requires,
      )
