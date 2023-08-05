import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ValidateInput", 
    version="0.0.1",
    author="6outtaTen",
    author_email="jacol.mucha@gmail.com",
    description="A module that validates whether the input text is a string or an integer",
    long_description="""This module contains 2 functions for user to use. It allows the user to validate whether the input is a string or an integer.
    Both functions have default values for the prompt text and the error message. These can be set while calling any function from the module. 
    These functions keep asking for the input and only finish when the input is correct. They of course return the input which can be assigned to a variable.
    To correctly import this module: from ValidateInput import ValidateInput
    Then you'll be able to access 2 functions: ValidateInput.validate_str() and ValidateInput.validate_int()
    """,
    long_description_content_type="text/markdown",
    url="https://github.com/6outtaTen/validateInput",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)