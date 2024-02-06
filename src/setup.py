"""Setup PyPi module"""
# pylint: disable=C0103

from setuptools import setup, find_packages

PLOOSH_VERSION = "0.1.11"

def setup_ploosh(name, install_requires):
    with open("../readme.md", encoding="UTF-8") as f:
        long_description = "".join(f.readlines())

    # replace relative link by absolute github link
    long_description = long_description.replace("(/", "(https://github.com/CSharplie/ploosh/blob/main/")

    install_requires = install_requires + [
            "colorama==0.4.6",
            "PyYAML==6.0.1",
            "Pyjeb==0.2.1",
            "pandas==2.1.4",
            "openpyxl==3.1.2",
            "sqlalchemy==1.4.51"
        ]

    setup (
        name = name,
        version = PLOOSH_VERSION,
        description="A framework to automatize your tests for data projects",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/CSharplie/ploosh/",
        project_urls={
            "Bug Tracker": "https://github.com/CSharplie/ploosh/issues",
            "CI": "https://github.com/CSharplie/ploosh/actions",
            "Documentation": "https://github.com/CSharplie/ploosh",
            "Source Code": "https://github.com/CSharplie/ploosh",
        },
        download_url="https://pypi.org/project/ploosh/",
        platforms="Any",
        python_requires=">=3.6",
        license= "Apache License 2.0",
        entry_points = {
            "console_scripts": [
                "ploosh = ploosh.__main__:main"
            ]
        },
        install_requires=install_requires,
    )