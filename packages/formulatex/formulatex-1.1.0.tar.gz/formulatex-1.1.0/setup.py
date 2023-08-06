from setuptools import setup, find_packages
from distutils.sysconfig import get_python_lib
import glob, os, sys

'''
     python setup.py sdist bdist_wheel
     python -m twine upload dist/* 
'''
STATIC_PATH = 'formulatex_src'
setup(
    name="formulatex",
    version='1.1.0',
    url='https://github.com/ThomasAtlantis/mathpix-formulatex',
    author='Shangyu Liu',
    author_email='liushangyu@sjtu.edu.cn',
    packages=["formulatex"],
    license='MIT',
    description="A web app to translate formulas into latex",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    keywords='latex mathpix formula',
    data_files=[
        (os.path.join(STATIC_PATH, 'templates'), glob.glob('templates/*.html')),
        (os.path.join(STATIC_PATH, 'statics'), ['statics/Calculation-64.ico'])
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
    install_requires=[
        'flask',
        'pyperclip',
        'gevent'
    ],
)