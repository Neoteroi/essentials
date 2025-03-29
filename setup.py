from setuptools import setup


def readme():
    with open("README.md") as f:
        return f.read()


setup(
    name="essentials",
    version="1.1.6",
    description="General purpose classes and functions",
    long_description=readme(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/Neoteroi/essentials",
    author="Roberto Prevato",
    author_email="roberto.prevato@gmail.com",
    keywords="core utilities",
    license="MIT",
    packages=["essentials", "essentials.typesutils", "essentials.decorators"],
    include_package_data=True,
)
