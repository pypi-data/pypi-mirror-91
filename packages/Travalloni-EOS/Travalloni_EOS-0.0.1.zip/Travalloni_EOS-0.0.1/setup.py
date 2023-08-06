from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='Travalloni_EOS',
  version='0.0.1',
  description='Travalloni generalized Equation of State',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Cosmos I Ikpoba',
  author_email='ikpobacosmos@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='Travalloni', 
  packages=find_packages(),
  install_requires=[''] 
)