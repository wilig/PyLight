from setuptools import setup, find_packages
import sys, os

version = '0.1'

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='pylight',
      version=version,
      description="A Python backend for LightTable",
      long_description=read('README.md'),
      classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: BSD License'],
      keywords='LightTable',
      author='will groppe',
      author_email='will.groppe@gmail.com',
      url='https://github.com/wilig/PyLight',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points={
        'console_scripts': [
            'pylight = pylight.tracer:exec_trace'
            ]
        },
      )
