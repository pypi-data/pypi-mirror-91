from setuptools import setup, find_packages

setup(
    name='JupyterNotebookReflection',
    version='0.0.2',
    description='A module to perform reflection coding in Jupyter notebooks.',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Charles Varley',
    license='MIT',
    keywords=['jupyter','notebook','reflection','introspection'],
    packages=find_packages(),
    install_requires=[''],
)