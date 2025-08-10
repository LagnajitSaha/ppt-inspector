#!/usr/bin/env python3
"""
Setup script for PowerPoint Inspector

This script allows users to install the PowerPoint Inspector tool
as a Python package for easy distribution and installation.
"""

from setuptools import setup, find_packages
import os

# Read the README file for long description
def read_readme():
    """Read README.md file for long description."""
    try:
        with open("README.md", "r", encoding="utf-8") as fh:
            return fh.read()
    except FileNotFoundError:
        return "PowerPoint Inspector - AI-powered tool for detecting inconsistencies in presentations"

# Read requirements from requirements.txt
def read_requirements():
    """Read requirements from requirements.txt file."""
    try:
        with open("requirements.txt", "r", encoding="utf-8") as fh:
            return [line.strip() for line in fh if line.strip() and not line.startswith("#")]
    except FileNotFoundError:
        return [
            "python-pptx>=0.6.21",
            "Pillow>=10.0.1",
            "google-generativeai>=0.3.2",
            "python-dotenv>=1.0.0",
            "click>=8.1.7",
            "rich>=13.7.0",
            "pandas>=2.1.4",
            "numpy>=1.24.3",
            "openpyxl>=3.1.2"
        ]

setup(
    name="ppt-inspector",
    version="1.0.0",
    author="PowerPoint Inspector Team",
    author_email="support@example.com",
    description="AI-powered tool for detecting inconsistencies in PowerPoint presentations",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ppt-inspector",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/ppt-inspector/issues",
        "Source": "https://github.com/yourusername/ppt-inspector",
        "Documentation": "https://github.com/yourusername/ppt-inspector#readme",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Office/Business",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
        ],
        "test": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "ppt-inspector=ppt_inspector:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.yml", "*.yaml"],
    },
    keywords=[
        "powerpoint",
        "presentation",
        "inconsistency",
        "detection",
        "ai",
        "gemini",
        "analysis",
        "validation",
        "quality",
        "audit"
    ],
    platforms=["any"],
    license="MIT",
    zip_safe=False,
)
