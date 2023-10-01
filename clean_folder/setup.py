from setuptools import setup

setup(
    name="clean_folder",
    version="0.1.0",
    description="script for sorting files",
    author="Igor SH",
    author_email="myemail@email.com",
    packages=["clean_folder"],
    entry_points={
        "console_scripts": [
            "clean_folder = clean_folder.clean:main_sorting_function",
        ],
    },
)
