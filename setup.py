from setuptools import setup, find_packages

version = "0.0.2"


with open("README.md") as f:
    readme = f.read()

setup(
    name="finage",
    version=version,
    description="Package to utilize Finage REST API",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/athompson1991/finage",
    author="Alex Thompson",
    author_email="alexthompson_1991@yahoo.com",
    maintainer="Alex Thompson",
    maintainer_email="alexthompson_1991@yahoo.com",
    keywords=["Finage", "finance", "stocks", "forex"],
    packages=find_packages(exclude=["test"]),
    install_requires=["requests"],
    license="MIT",
    classifiers=[
        'Programming Language :: Python :: 3.9'
    ]
)
