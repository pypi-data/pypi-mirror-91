from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='balinese_library',
  version='0.0.6',
  description='A very basic balinese library about information extraction in balinese language',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  packages=['balinese_library'],
  package_data={'balinese_library': ['storage/BaliVocab.txt'], 'balinese_library': ['storage/hmmmodel.txt'], 'balinese_library': ['storage/sansekertavocab.txt'] },
  author='Ngurah Agus Sanjaya ER',
  author_email='agus_sanjaya@unud.ac.id',
  license='MIT', 
  classifiers=classifiers,
  keywords='Information Extraction, Balinese', 
  install_requires=['nltk'] 
)