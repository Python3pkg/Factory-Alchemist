from setuptools import setup, find_packages
from sqlalchemy_mommy import __version__


setup(name='SQLAlchemy-mommy',
      version=__version__,
      packages=find_packages(exclude=['*test*']),
      url='https://github.com/eduardo-matos/SQLAlchemy-mommy',
      author='Eduardo Matos',
      keywords='sql sqlalchemy modelmommy orm')
