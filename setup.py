from setuptools import setup, find_packages

# Read the long description from README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="django-react-jollof",  # Unique name for your package
    version="1.0.1",  # Version of your package
    author="Temitope Kayode",  # Your name
    author_email="cwt@temilimited.com",  # Your email
    description="A CLI tool to scaffold Django + React projects with options for social login and styling frameworks.",
    long_description=long_description,  # Use the README for the long description
    long_description_content_type="text/markdown",  # Specify Markdown format
    url="https://github.com/sir-temi/django-react-jollof",  # Link to your repository
    license="MIT",  # License type
    license_files=["LICENSE"],  # Explicitly include the license
    packages=find_packages(
        exclude=["tests", "*.tests", "*.tests.*", "tests.*"]
    ),  # Automatically find all packages
    include_package_data=True,  # Include non-Python files (e.g., templates)
    package_data={
        "django_react_jollof": ["templates/**/*"],  # Include templates recursively
    },
    install_requires=[
        "click>=8.0",  # CLI functionality
        "requests>=2.0",  # HTTP requests
        "python-decouple>=3.6",  # Managing environment variables
        "djangorestframework>=3.13",  # Django REST framework
        "djangorestframework-simplejwt>=5.2",  # JWT Authentication
        "django-cors-headers>=3.13",  # CORS for Django
        "django-allauth>=0.53",  # Social authentication
    ],
    extras_require={
        "dev": [
            "flake8>=4.0",  # For linting
        ]
    },
    entry_points={
        "console_scripts": [
            "django-react-jollof=django_react_jollof.cli:cli",  # CLI command setup
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",  # Package maturity
        "Environment :: Console",
        "Framework :: Django",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="django react cli scaffolding jwt social-auth",  # Keywords for discoverability
    python_requires=">=3.10",  # Minimum Python version required
    project_urls={
        "Bug Tracker": "https://github.com/sir-temi/django-react-jollof/issues",
        "Documentation": "https://github.com/sir-temi/django-react-jollof#readme",
        "Source Code": "https://github.com/sir-temi/django-react-jollof",
        "Changelog": "https://github.com/sir-temi/django-react-jollof/releases",
    },
)
