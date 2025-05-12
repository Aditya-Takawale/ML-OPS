from setuptools import setup, find_packages

# Read requirements from file
with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

# Read project description from README file
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="Hotel-Reservation-Prediction",
    version="0.1",
    author="Kunjesh",
    author_email="your_email@example.com",  # Add your email (optional)
    description="A Hotel Reservation Prediction system using MLOps.",
    long_description=long_description,
    long_description_content_type="text/markdown",  # Important for README formatting
    packages=find_packages(),
    install_requires=requirements,
    python_requires=">=3.7",  # Ensure compatibility with Python versions
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
