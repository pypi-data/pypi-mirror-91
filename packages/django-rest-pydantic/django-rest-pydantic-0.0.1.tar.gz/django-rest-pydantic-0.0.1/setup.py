from setuptools import setup, find_packages


def readme():
    with open("README.md", "r") as infile:
        return infile.read()


classifiers = [
    "Development Status :: 1 - Planning",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
]

install_requires = []

setup(
    name="django-rest-pydantic",
    version="0.0.1",
    description="",
    long_description=readme(),
    long_description_content_type="text/markdown",
    keywords="",
    license="MIT",
    url="https://github.com/phillipdupuis/django-rest-pydantic",
    author="Phillip Dupuis",
    author_email="phillip_dupuis@alumni.brown.edu",
    packages=[],
    install_requires=install_requires,
    classifiers=classifiers,
)
