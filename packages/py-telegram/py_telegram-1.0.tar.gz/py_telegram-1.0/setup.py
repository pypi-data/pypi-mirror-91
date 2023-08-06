import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py_telegram",
    version="1.0",
    author="Gabriel Heinzer",
    author_email="dev@gabrielheinzer.ch",
    description="This module should help you controlling the telegram bot API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/programmer372/python-telegram-api",
    packages=setuptools.find_packages(),
    # classifiers=[
        #"Programming Language :: Python :: 3",
        #"License :: OSI Approved :: MIT License",
        #"Operating System :: OS Independent",
    # ],
    python_requires=">=3.0",
    include_package_data=True
)
