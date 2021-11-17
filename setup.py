from setuptools import setup, find_packages


setup(
    name='tweesky',
    version='0.0.1',
    license='MIT',
    author="Beppe Catanese",
    author_email='beppe.catanese@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/gcatanese/Tweesky',
    keywords='OpenGraph, Twitter, Social Media',
    install_requires=[
        'requests==2.26.0',
        'spotipy==2.19.0',
        'python-dotenv===0.19.2',
        'beautifulsoup4===4.10.0',
        'requests-html===0.10.0',
        'selenium===4.0.0',
        'Pillow===8.4.0'
      ],

)