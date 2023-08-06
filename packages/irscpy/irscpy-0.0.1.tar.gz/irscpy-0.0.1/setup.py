import setuptools

with open("README.txt", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="irscpy", # Replace with your own username
    version="0.0.1",
    author="Armin Dadras Eslamlou",
    author_email="armindadraseslamlou@gmail.com",
    description="An earthquake data package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ArminDadras",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)