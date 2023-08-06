from distutils.core import setup

version = '0.2.11'
name = 'python_helper'
url = f'https://github.com/SamuelJansen/{name}/'

setup(
    name = name,
    packages = [
        name,
        f'{name}/api',
        f'{name}/api/src',
        f'{name}/api/src/service',
        f'{name}/api/src/domain',
        f'{name}/api/src/helper',
        f'{name}/api/src/annotation'
    ],
    version = version,
    license = 'MIT',
    description = 'python helper package',
    author = 'Samuel Jansen',
    author_email = 'samuel.jansenn@gmail.com',
    url = url,
    download_url = f'{url}archive/v{version}.tar.gz',
    keywords = ['helper', 'python helper package', 'python helper', 'helper package'],
    install_requires = [
        'colorama==0.4.3'
    ],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9'
    ]
)
