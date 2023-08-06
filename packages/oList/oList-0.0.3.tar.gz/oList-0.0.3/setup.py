import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="oList", # Replace with your own username
    version="0.0.3",
    author="Marc D",
    author_email="marcwarrelldavis@yahoo.com",
    description="A Python 'Object List'. It's basically your standard python list that additionally lets you attach data to it that doesn't affect the actual list items itself.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mwd1993/oList",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)