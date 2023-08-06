import setuptools

with open("README.rst", "r") as file:
    long_description=file.read()

setuptools.setup(
    name="coder-vk-pagkac",
    version="1.2",
    author="Vikram Shinde",
    author_email="sinden@gmail.com",
    description="Python project for testing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://moviesstream.vip",
    packages=setuptools.find_packages(exclude=['tests*']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=2.7',
    include_package_data=True,
    install_requires=[]
)