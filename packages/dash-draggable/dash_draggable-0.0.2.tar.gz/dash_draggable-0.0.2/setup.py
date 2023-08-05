import json
import os
from setuptools import setup


with open('package.json') as f:
    package = json.load(f)

package_name = package["name"].replace(" ", "_").replace("-", "_")

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name=package_name,
    version=package["version"],
    author=package['author'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=package['homepage'],
    packages=[package_name],
    include_package_data=True,
    license=package['license'],
    description=package.get('description', package_name),
    install_requires=[],
    classifiers = [
        'Framework :: Dash',
    ],    
)
