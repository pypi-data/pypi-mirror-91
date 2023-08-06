from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="dominisia",
    version="0.0.1",
    description="Say hello!",
    py_modules=["dominisia"],
    package_dir={'':'src'},
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: POSIX :: Linux",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pawlaczyk/dominisia",
    author="Dominika Pawlaczyk",
    autor_email="dominika.pawlaczyk9@gmail.com",
)