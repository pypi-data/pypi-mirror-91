from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

setup(
  name='datecalculator',
  version='0.0.1',
  description='calculate how many years,month and days between time you entered and now ',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='mohammed yasser',
  author_email='muhammedyasser85@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='date calculator', 
  packages=find_packages(),
  install_requires=['datetime'] 
)