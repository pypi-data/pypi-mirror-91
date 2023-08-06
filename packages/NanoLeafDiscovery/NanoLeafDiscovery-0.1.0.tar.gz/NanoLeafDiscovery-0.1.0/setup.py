from setuptools import setup, find_packages
import NanoLeafDiscovery

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

setup(
  name='NanoLeafDiscovery',
  version='0.1.0',
  description='Discovery module for nanoleaf',
  long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
  long_description_content_type='text/markdown',
  url='https://github.com/NotBlue-Dev/NanoLeaf-Discovery',
  author='NotBlue',
  author_email='',
  license='MIT',
  classifiers=classifiers,
  keywords='nanoleaf',
  packages=find_packages(),
  install_requires=['requests']
)