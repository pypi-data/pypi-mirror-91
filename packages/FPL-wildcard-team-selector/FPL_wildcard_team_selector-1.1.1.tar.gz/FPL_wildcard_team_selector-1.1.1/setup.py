import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='FPL_wildcard_team_selector',
    version='1.1.1',
    author='Abdulrahman Elgendy',
    author_email='Abdul.Elgendy@outlook.com',
    description='This package helps you select the best 15 players to choose when playing a wildcard on Fantasy premier league on any given week',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/abdul-gendy/FPL_wildcard_team_selector',
    download_url="https://github.com/abdul-gendy/FPL_wildcard_team_selector/archive/v1.1.1.tar.gz",
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=['PuLP==2.3.1',
                      'beautifulsoup4==4.9.3',
                      'lxml==4.6.2',
                      'requests==2.25.0',
                      'pandas==1.1.4'],
    python_requires='>=3.6',
)
