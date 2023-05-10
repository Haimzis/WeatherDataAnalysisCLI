from setuptools import setup, find_packages

setup(
    name='WeatherCLI',
    version='1.0a',
    description='A command-line tool for doing something useful',
    author='Haim',
    author_email='Haimzismann@gmail.com',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'WeatherCLI=WeatherCLI.__main__:main',
        ],
    },
    install_requires=open('requirements.txt').readlines(),
)