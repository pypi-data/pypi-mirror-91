import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="taller-openwebinar",
    version="2.0.0",
    description="Definicion de Openwebinar",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Tlalocan-Courses/Taller-publica-un-paquete-en-Pypi",
    author="OpenWebinars",
    author_email="openwebinars@openwebinars.net",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["openwebinars"],
    #packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=["python-string-utils"],
    entry_points={
        "console_scripts": [
            "openwebinars=openwebinars.__main__:main",
        ]
    },
)
