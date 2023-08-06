import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fdscraper", # Replace with your own username
    version="0.0.1",
    author="Chinmay Kurade",
    author_email="chinmay.v.kurade@gmail.com",
    description="A Web scrapping tool for stock fundamentals data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chinmaykurade/fdscraper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)