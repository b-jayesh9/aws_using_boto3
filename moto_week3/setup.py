from setuptools import setup, find_packages

setup(
    name='moto_week3',
    version='1.0.0',
    description="sample project for Moto3 implementation",
    author="Jayesh Bhatia",
    author_email="abc@yz.oco",

    packages=find_packages(
        exclude=['tests']
    ),

    test_suite='tests',

    install_requires=['boto3', 'unittest-xml-reporting'],

    tests_require=['moto'],

    entry_points={
        'console_scripts' : [
            's3 = buck01jay.s3:main',
        ]

    },


)