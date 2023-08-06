from distutils.core import setup
# from setuptools import setup, find_packages

setup(
    name='haetek_algo_new',
    version='1.0.0',
    py_modules=['haetek_algo_new'],
    # packages=find_packages(),
    author='haetek_shenzhen',
    author_email='haetek123@163.com',
    url='https://haetek.com/',
    description='Haetek Algorithm Platform',
    data_files=[('Lib/site-packages', ["api_info_2021jan13.json"])]
)