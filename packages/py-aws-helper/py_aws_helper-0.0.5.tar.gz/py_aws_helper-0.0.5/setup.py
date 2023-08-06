from setuptools import setup, find_packages

requires = [
    'boto3'
]


setup(
    name='py_aws_helper',
    version='0.0.5',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='Helper for AWS services like S3 written in python...',
    long_description=open('README.rst').read(),
    install_requires=requires,
    url='https://github.com/1CloudHub/py_aws_helper.git',
    author='Sripranav P',
    author_email='sripranav@1cloudhub.com'
)
