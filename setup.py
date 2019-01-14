from setuptools import setup

with open('README.rst', 'r') as f:
    long_description = f.read()

setup(
    name='Decision-Tree-Generator',
    version='0.0.4',
    packages=['decision_tree'],
    package_dir={'decision_tree': 'src/decision_tree'},
    url='https://github.com/KYDronePilot/Decision-Tree-Generator',
    license='GPL-3.0',
    long_description=long_description,
    author='KYDronePilot',
    author_email='33381603+KYDronePilot@users.noreply.github.com',
    description='Program for generating decision tree LaTeX code for array-based algorithms'
)
