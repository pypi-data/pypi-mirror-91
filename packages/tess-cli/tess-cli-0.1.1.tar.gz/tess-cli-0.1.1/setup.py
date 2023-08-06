import setuptools

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='tess-cli',
    version='0.1.1',
    author='Andres Martinez',
    author_email='andressbox90@gmail.com',
    description='CLI tool for testing algorithms.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/andresscode/tess',
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS'
    ],
    python_requires='>=3.7',
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        tess=tess.src.cli:main
    '''
)
