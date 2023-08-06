import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="classInfo",
    version="1.0.1",
    author="WinXpDev",
    author_email="muhammad184276@gmail.com",
    description="classInfo is useful to write information about everything(almost)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/IM-code111/jsonbase-1.0.0",
    packages=setuptools.find_packages(),
    py_modules=['classInfo'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)