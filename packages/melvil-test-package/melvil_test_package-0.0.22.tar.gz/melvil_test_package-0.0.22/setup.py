import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="melvil_test_package",
    version="0.0.22",
    author="Melvil James",
    author_email="madapoor@gmailc.com",
    description="Plays alarm when long script finishes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Tina-Bu/dingpy/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
