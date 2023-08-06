import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hackertype", # Replace with your own username
    version="0.1",
    author="Denis Daletski",
    author_email="daletskidenis@gmail.com",
    description="Type like a holywood movie hacker",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ddaletski/hackertype",

    py_modules=['hackertype'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        hackertype=hackertype:cli
    '''
)
