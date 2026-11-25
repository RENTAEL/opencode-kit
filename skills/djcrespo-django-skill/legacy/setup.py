#!/usr/bin/env python3
"""
Setup configuration for Django Dev Pro Skill
Allows installation via pip or setuptools
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_file.exists():
    with open(requirements_file, 'r') as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="django-dev-pro",
    version="1.0.0",
    author="djcrespo",
    author_email="dev@djcrespo.com",
    description="Automatiza el flujo completo de desarrollo con Django REST Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/djcrespo/django-skill",
    license="MIT",
    packages=find_packages(where="lib"),
    package_dir={"": "lib"},
    python_requires=">=3.10",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "django-dev-pro=main:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: Spanish",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Build Tools",
    ],
    keywords="django drf automation code-generation testing",
    project_urls={
        "Bug Reports": "https://github.com/djcrespo/django-skill/issues",
        "Documentation": "https://github.com/djcrespo/django-skill",
        "Source Code": "https://github.com/djcrespo/django-skill",
    },
)
