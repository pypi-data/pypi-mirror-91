from pathlib import Path
from setuptools import setup, find_packages

with open(Path("./README.md")) as f:
    readme_text = f.read()

setup(
    name="woptics",
    version="0.0.1",
    description="Light propogation simluation, using the scalar wave propogation approximation",
    long_description=readme_text,
    long_description_content_type="text/markdown",
    url="https://github.com/rjkilpatrick/woptics",
    author="John Kilpatrick",
    author_email="john.kilpatrick@outlook.com",
    license="MIT",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Physics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Science/Research",
    ],
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    python_requires=">=3.4",
    install_requires=["numpy", "matplotlib", "scipy"],
)
