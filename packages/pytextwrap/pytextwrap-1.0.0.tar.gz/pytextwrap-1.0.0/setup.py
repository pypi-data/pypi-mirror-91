import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytextwrap",
    version="1.0.0",
    author="Tushar Sadhwani",
    author_email="tushar.sadhwani000@gmail.com",
    description="Wraps text without breaking words.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tusharsadhwani/pytextwrap",
    py_modules=['pytextwrap'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': ['textwrap=pytextwrap:cli'],
    }
)
