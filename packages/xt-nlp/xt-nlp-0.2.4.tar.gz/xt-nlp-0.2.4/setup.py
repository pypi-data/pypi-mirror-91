import setuptools, os

PACKAGE_NAME = 'xt-nlp'
VERSION = '0.2.4'
AUTHOR = 'Xtract AI'
EMAIL = 'info@xtract.ai'
DESCRIPTION = 'Utilities for training and working with nlp models in pytorch'
GITHUB_URL = 'https://github.com/XtractTech/xt-nlp'

parent_dir = os.path.dirname(os.path.realpath(__file__))

with open(f'{parent_dir}/README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name=PACKAGE_NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=EMAIL,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=GITHUB_URL,
    packages=[
        'xt_nlp',
        'xt_nlp.utils',
    ],
    provides=['xt_nlp'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'transformers',
        'numpy',
        'torch',
        'scikit-learn',
        'xt-training'
    ],
)
