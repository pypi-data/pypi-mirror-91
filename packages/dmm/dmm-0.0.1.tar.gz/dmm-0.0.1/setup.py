from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='dmm',
    version='0.0.1',
    description='DMM API Client for Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Ippei Matsubara',
    author_email='matz1ppei@gmail.com',
    url='https://github.com/matz1ppei/dmm',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    install_requires=['requests'],
    tests_require=['pytest', 'pytest-cov', 'pytest-flake8']
)
