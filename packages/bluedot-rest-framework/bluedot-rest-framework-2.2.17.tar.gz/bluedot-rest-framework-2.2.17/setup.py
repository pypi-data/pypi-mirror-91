import os
from setuptools import setup, find_packages


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]


def get_package_data(package):
    """
    Return all files under the root package, that are not in a
    package themselves.
    """
    walk = [(dirpath.replace(package + os.sep, '', 1), filenames)
            for dirpath, dirnames, filenames in os.walk(package)
            if not os.path.exists(os.path.join(dirpath, '__init__.py'))]

    filepaths = []
    for base, filenames in walk:
        filepaths.extend([os.path.join(base, filename)
                          for filename in filenames])
    return {package: filepaths}


setup(
    name='bluedot-rest-framework',
    version='2.2.17',
    packages=get_packages('bluedot-rest-framework'),
    package_data=get_package_data('bluedot-rest-framework'),
    include_package_data=True,
    zip_safe=True,
    install_requires=[
        'psycopg2',
        'django',
        'djangorestframework',
        'djangorestframework-jwt',
        'redis',
        'uwsgi',
        'oss2',
        'pdf2image',
        'channels == 2.4',
        'channels-redis == 2.4.2',
        'wechatpy',
        'websocket_client',
    ],
)
