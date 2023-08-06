from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='vdevapi',
  version='0.0.3',
  description='An API, that can do a lots of cool things.',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Michael Ďalog',
  author_email='michaelvertexxdalog@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='api', 
  packages=find_packages(),
  install_requires=['requests'] 
)
