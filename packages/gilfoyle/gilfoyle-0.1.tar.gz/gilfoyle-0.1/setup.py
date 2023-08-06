from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='gilfoyle',
    packages=['gilfoyle'],
    version='0.01',
    license='MIT',
    description='Gilfoyle is a Python-based report generator for data scientists who use Pandas.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Matt Clarke',
    author_email='matt@flyandlure.org',
    url='https://github.com/flyandlure/gilfoyle',
    download_url='https://github.com/flyandlure/gilfoyle/archive/master.zip',
    keywords=['python', 'reports', 'reporting', 'pandas'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
    install_requires=['pandas', 'weasyprint', 'jinja2', 'pprint']
)
