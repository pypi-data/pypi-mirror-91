import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fivem.py",  # Replace with your own username
    version="0.0.1",
    author="github.com/Wiper-R",
    author_email="rshivang12345@gmail.com",
    description="FiveM API Wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypi/",
    packages=['async_fivem'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
