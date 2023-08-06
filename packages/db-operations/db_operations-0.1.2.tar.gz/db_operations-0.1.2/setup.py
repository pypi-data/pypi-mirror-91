from setuptools import setup

setup(name='db_operations',
      version='0.1.2',
      author='K.lz',
      author_email='565150134@qq.com',
      description='Simple operation of database',
      url='https://github.com/kimkimheel',
      packages=['db_operations'],
      install_requires=['pymysql','pymssql','cx_Oracle'],
      zip_safe=False)