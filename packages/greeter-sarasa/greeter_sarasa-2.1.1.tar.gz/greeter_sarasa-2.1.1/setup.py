import pathlib
from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="greeter_sarasa",
    version="2.1.1",
    description="Greets people",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/maartincm/greeter",
    author="Martin Cuesta",
    author_email="cuesta.martin.n@hotmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(include=["greeter"]),
    include_package_data=True,
    install_requires=["PyYAML==5.3.1"],
    entry_points={
        "console_scripts": [
            "greet=greeter.__main__:main",
        ]
    },
)
