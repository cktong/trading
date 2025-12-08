#!/usr/bin/env python3
"""
Setup script for Crypto Backtest Engine
"""

from setuptools import setup, find_packages
import os

# Read README for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="crypto-backtest-engine",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Universal cryptocurrency backtesting engine with support for 200+ assets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cktong/crypto-backtest-engine",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Developers",
        "Topic :: Office/Business :: Financial :: Investment",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=3.0",
            "black>=22.0",
            "flake8>=4.0",
            "mypy>=0.950",
        ],
        "notebook": [
            "jupyter>=1.0",
            "ipywidgets>=7.6",
        ],
    },
    entry_points={
        "console_scripts": [
            "crypto-backtest=examples.quick_start:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.ipynb"],
    },
    keywords=[
        "cryptocurrency", 
        "bitcoin", 
        "ethereum", 
        "trading", 
        "backtest", 
        "backtesting",
        "algorithmic-trading",
        "trading-strategies",
        "technical-analysis",
        "hyperliquid",
        "spdr",
        "glam",
    ],
    project_urls={
        "Bug Reports": "https://github.com/cktong/crypto-backtest-engine/issues",
        "Source": "https://github.com/cktong/crypto-backtest-engine",
        "Documentation": "https://github.com/cktong/crypto-backtest-engine/blob/main/README.md",
    },
)
