import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="passwordtools",
    version="0.0.6",
    author="TriC",
    author_email="parantezdev@gmail.com",
    description='Fast password module using the "io" and "random" modules.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ConConDiscord/passwordtools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
