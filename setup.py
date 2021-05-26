import setuptools


#with open("README.rst", "r") as file:
#    long_description = file.read()
long_description = "Easily protect your serialized class objects with secure encryption. Kosher Pickles provides a Mixin you can use in any classes you wish to protect."

setuptools.setup(
    name='kosher',
    version='0.1.6',
    author="Forest Mars",
    author_email="themarsgroup+pypi@gmail.com",
    description="Encrypted Pickles",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Apache 2.0",
    url="https://github.com/forestmars/kosher",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
         ],
    )
