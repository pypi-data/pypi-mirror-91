"""Build and install pytest-django-ifactory."""

from setuptools import setup, find_packages

with open("README.md", "r") as stream:
    long_description = stream.read()

setup(
    name="pytest-django-ifactory",
    version="0.4.0",
    author="Mattias Jakobsson",
    author_email="mjakob422@gmail.com",
    description="A model instance factory for pytest-django",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/gorilladev/pytest-django-ifactory",
    license="BSD-3-Clause",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Plugins",
        "Framework :: Django",
        "Framework :: Pytest",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Testing",
    ],
    keywords="pytest django database testing",
    packages=find_packages(exclude=["tests*"]),
    install_requires=["Django", "pytest-django"],
    entry_points={"pytest11": ["django-ifactory = pytest_django_ifactory.plugin"]},
)
