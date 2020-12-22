import setuptools


with open("README.rst", "r") as file:
    long_description = file.read()


setuptools.setup(
    name='kosher',
    version='0.1',
    scripts=['mixins.py'] ,
    author="Forest Mars",
    author_email="themarsgroup+kosher@gmail.com",
    description="Encrypted Pickles",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/forestmars/kosher",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache License",
        "Operating System :: OS Independent",
         ],
    )
