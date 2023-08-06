from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='mongoc',
    version='0.3',
    description='A fast way to view databases, collections and documents from mongodb in the command line',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/JakeRoggenbuck/mongoc',
    author='Jake Roggenbuck',
    author_email='jake@jr0.org',
    license='MIT',
    py_modules=['mongoc'],
    install_requires=required,
    zip_safe=False,
    entry_points={'console_scripts': ['mongoc = mongoc:main']},
)
