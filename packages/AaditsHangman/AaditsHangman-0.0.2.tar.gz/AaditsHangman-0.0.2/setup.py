import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="AaditsHangman", # Replace with your own username
    version="0.0.2",
    author="Aadit Bansal",
    author_email="aaditisawesome@gmail.com",
    description="A hangman game created on tkinter python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aaditisawesome/hangman",
    packages=setuptools.find_packages(),
    install_requires=['RandomWords'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)