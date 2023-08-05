import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hcpa-biomed-processing",
    version="1.0.1",
    author="Rafael de Freitas",
    author_email="dfr.rafael@gmail.com",
    description="Apply color deconvolution and threshold on selected images",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RafaelFreita/hcpa-image-processing",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)