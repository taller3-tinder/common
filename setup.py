from setuptools import setup, find_packages

setup(
    name='tinderlibs',
    version='0.1.1',
    packages=find_packages(),
    author='Tinder - Taller3',
    author_email='mcapon@fi.uba.ar',
    description='Paquetes common al backend de Taller',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/taller3-tinder/tinderlibs',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
