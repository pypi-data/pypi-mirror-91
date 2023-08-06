import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="suntimes", 
    version="0.2.2",
    author="Paul Mathis",
    author_email="pmathis@protonmail.com",
    description="For a given place (longitude, latitude and altitude) and a given day, returns the time of sunrise and the time of sunset (in UTC and in local time). Create and save a json or csv file with the timetables for a whole year.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/p-mathis/suntimes",
    packages=setuptools.find_packages(),
    install_requires=['pytz',
                      'tzlocal',
                      'jdcal',                     
                      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
