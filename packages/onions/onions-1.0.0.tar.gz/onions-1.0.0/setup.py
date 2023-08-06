from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='onions',
    version='1.0.0',
    description='useless module',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='HYKANTUS',
    author_email='hykantus@gmail.com',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
    ],

    keywords='useless',
    packages=find_packages(),
    python_requires='>=3.6, <4',
    install_requires=[],
    project_urls={
        'Personal Website': 'http://hykantus.tk/',
    },
)
