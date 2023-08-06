import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="BankDataInvestigation", # Replace with your own username
    
    version="1.0.2",
    
    author="Nesrine Yousfi",
    
    author_email="yousfi.nesrine@gmail.com",
    
    description="This is a python package to Investigate in Bank data using Pansdas and Pyspark, made while an MHPC thesis  in ICTP/SISSA and Prometeia",
    
    long_description=long_description,
    
    long_description_content_type="text/markdown",
    
    url="https://gitlab.com/yousfi.nesrine/prometeia_project.git",
    
    packages=setuptools.find_packages(),
    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
