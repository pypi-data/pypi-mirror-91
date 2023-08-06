import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ahccchatbot",
    version="0.0.2",
    author="Raja Sur",
    author_email="rajasur90@gmail.com",
    description="A small library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    #url="https://github.com/Ajayff4/testing2",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)