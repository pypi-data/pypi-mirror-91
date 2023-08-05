import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python_lic_sys", # Replace with your own username
    version="0.0.3",
    author="TechSmit",
    author_email="techsmitdevloper@gmail.com",
    description="A Easy Softwear Licensing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PythonProgramme/Python-Code",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
