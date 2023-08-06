import setuptools
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="view-logger",
    version="0.9",
    author="J4CK VVH173, Polosha",
    author_email="i78901234567890@gmail.com",
    description="Package with decorators for views",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/J4CKVVH173/view-logger",
    packages=setuptools.find_packages(),
    install_requires=[],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
        "Framework :: Django"
    ],
    python_requires='>=3.6',
)
