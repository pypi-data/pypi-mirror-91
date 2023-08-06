from setuptools import setup, find_packages


setup(
    name="pysport",
    version="1.0.2",
    author="Sarang Purandare",
    author_email="purandare.sarang@gmail.com",
    description="An efficient web scraping library for everything sports",
    long_description="An efficient web scraping library for everything sports (currenlty supports https://www.premierleague.com/ and https://www.sofascore.com/",
    long_description_content_type="text/markdown",
    packages=['pysport'],
    install_requires=[
        'pandas',
        'requests' 
    ],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ]
)