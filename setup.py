import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simple_ad", # Replace with your own username
    version="0.0.5",
    author="Eric Longstreet",
    author_email="elongstreet88@gmail.com",
    description="A simple Active Directory Python module to reduce boilerplate and increase productivity.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/elongstreet88/Python_Simple_AD",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)