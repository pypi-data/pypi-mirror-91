import setuptools

with open ("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
setuptools.setup (
    name = 'nester_tt',
    version = '1.0.0',
    py_modules = ['nester_tt'],
    author = 'hotchups',
    author_email = 'miyoungkim.1126@gmail.com',
    description = 'A simple printer of nested lists',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    )
