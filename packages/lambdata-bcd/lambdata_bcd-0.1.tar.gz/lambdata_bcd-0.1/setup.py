import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lambdata_bcd", # Replace with your own username
    version="0.1",
    author="Brett",
    description="A Lambda School assignment",
    url="https://github.com/doffing81/lambdata",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
          'numpy',
          'pandas',
    ],
    python_requires='>=3.6',
)
