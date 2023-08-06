from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name='cookie2json',
    version='1.1',
    packages=find_packages(),
    url='https://github.com/mlzxgzy/cookie2json/',
    license='MIT',
    author='Kami',
    author_email='kami@kdajv.com',
    description='format cookies from chrome or firefox to json.',
    long_description=long_description,
    long_description_content_type="text/markdown",
)
