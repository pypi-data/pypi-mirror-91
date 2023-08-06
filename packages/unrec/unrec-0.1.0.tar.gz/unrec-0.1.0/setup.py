
from setuptools import setup

with open("./README.md", encoding = "utf-8") as f:
    long_description = f.read()

setup(
    name = "unrec",
    version = "0.1.0",
    description = "This is a tool to fix recursive calls to loop in a fully automatic manner.",
    author = "TTLab",
    author_email = "t.tools.lab@gmail.com",
    url = "https://github.co.jp/",
    packages = ["unrec"],
    install_requires = ["relpath"],
    long_description = long_description,
    long_description_content_type = "text/markdown",
    license = "CC0 v1.0",
    classifiers = [
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries",
        "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication"
    ],
    # entry_points = """
    #     [console_scripts]
    #     tskr = tskr:tskr
    # """
)
