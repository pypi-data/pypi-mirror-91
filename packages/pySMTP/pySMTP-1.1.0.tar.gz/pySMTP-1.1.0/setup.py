from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='pySMTP',
    version='1.1.0',
    description='An easy-to-use python library to send emails within seconds',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/HYKANTUS/pySMTP/',
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

    keywords='email, gmail, smtp, smtplib, gmail smtp',
    packages=find_packages(),
    python_requires='>=3.6, <4',
    install_requires=[],
    project_urls={
        'Personal Website': 'http://hykantus.tk/',
    },
)
