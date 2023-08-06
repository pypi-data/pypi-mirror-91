import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-social-layer',
    version='0.0.8',
    packages=find_packages(),
    include_package_data=True,
    license='GNU License',  # example license
    description='Adds social media features to any website',
    long_description=README,
    long_description_content_type='text/x-rst',
    url='https://github.com/gsteixeira',
    author='Gustavo Selbach Teixeira',
    author_email='gsteixei@gmail.com',
    zip_safe=False,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        ],
    install_requires=[
        'django-mediautils>=0.1.0',
        ],
    package_data={
            'social_layer': ['social_layer/migrations/*',]
        },
)
