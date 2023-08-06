import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="corncob",
    version="0.0.1",
    author="Jonathan Golob",
    author_email="j-dev@golob.org",
    description="beta-binomial based testing of count data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jgolob/corncob",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points = {
        'console_scripts': ['cc_bbdml=corncob.command_line:main'],
    },
    install_requires=[
        'pandas',
        'scipy',
        'numpy',
        'statsmodels'
    ],
)
