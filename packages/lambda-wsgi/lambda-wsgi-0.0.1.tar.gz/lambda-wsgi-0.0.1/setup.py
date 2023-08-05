from setuptools import setup

with open('README.md') as file:
    long_description = file.read()

setup(
    name='lambda-wsgi',
    version='0.0.1',
    author='Amit Marcus',
    author_email='marxus@gmail.com',
    description='run wsgi apps on aws lambda from api gateway or alb events',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/marxus/lambda-wsgi',
    packages=['lambda_wsgi']
)
