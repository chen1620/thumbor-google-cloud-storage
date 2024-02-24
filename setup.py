from setuptools import setup, find_packages
import os

def version():
    """retrieve version from tag name"""
    github_ref_name = os.getenv('GITHUB_REF_NAME')
    if github_ref_name is not None:
        return github_ref_name
    return '0.0.1'

def readme():
    """print long description"""
    with open('README.md') as f:
        return f.read()

setup(
    name='tc_gcs',
    version=version(),
    packages=find_packages(),
    author='Ngo Sach Nhat (Chen)',
    author_email='nhatns.uet@gmail.com',
    description='A simple Thumbor custom storage for Google Cloud Storage',
    long_description=readme(),
    long_description_content_type='text/markdown',
    license='MIT',
    keywords='thumbor gcs google cloud storage',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'thumbor>=7.6.0',
        'google-cloud-storage>=2.14.0',
    ],
)
