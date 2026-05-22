from setuptools import setup, find_packages

setup(
    name="pokesdk",
    version="0.2.0",
    description="A lightweight ETL SDK for the PokéAPI",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "requests>=2.28",
        "pandas>=2.0",
    ],
    extras_require={
        "parquet": ["pyarrow>=14.0"],
        "dev": ["pytest>=7", "responses>=0.25"],
    },
)
