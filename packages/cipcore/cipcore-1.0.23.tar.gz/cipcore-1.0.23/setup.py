from setuptools import setup, find_packages

VERSION='1.0.23'
PACKAGES=find_packages()
    #['cipcore', 'cipcore.V2']

setup(name='cipcore',
      version=VERSION,
      description='CIP core classes.',
      author='CIP Team',
      author_email='gustavo.oliveira@tvlgobo.com.br',
      license='MIT',
      packages=PACKAGES,
      install_requires=[
          'mock==2.0.0',
          'requests==2.18.4',
          'ciperror==1.0.52',
          'pytest==5.0.1',
          'responses==0.10.6',
          'coverage==4.5.3',
          'cip-workflow-status==0.0.19',
          'PyHamcrest==1.9.0',
          'redis==3.1.0',
          'fakeredis==1.0.2'
      ],
      zip_safe=False)
