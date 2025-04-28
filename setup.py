from setuptools import setup, find_packages

setup(
    name="stockmarketproject",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "dearpygui",
        "yfinance",
        "tzlocal",
        "yahooquery",
        "pytz",
        "pandas",
        "numpy",
        "plotly",
        "pytest",
        "pytest-mock"
    ],
    python_requires=">=3.8",
) 