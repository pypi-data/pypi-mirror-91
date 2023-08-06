import os
from setuptools import setup, find_packages
import djangocms_headings


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='djangocms-headings',
    version=djangocms_headings.__version__,
    author='Sasha Matijasic',
    author_email='sasha@selectnull.com',
    packages=find_packages(),
    url='https://github.com/selectnull/djangocms-headings',
    license='MIT',
    description='djangocms plugin that implements HTML headings',
    long_description_content_type='text/markdown',
    long_description=open('README.md').read(),
    include_package_data=True,
    install_requires=[
        'django-cms>=3.6'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
