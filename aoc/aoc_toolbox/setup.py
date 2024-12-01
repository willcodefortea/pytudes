from setuptools import find_packages, setup

setup(
    name="aoc",
    version="0.1.0",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=[
        "click",
    ],
    entry_points={
        "console_scripts": [
            "aoc = aoc:cli",
        ],
    },
)
