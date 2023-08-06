from setuptools import setup, find_packages

setup(
    name="shuttl-time",
    version="0.0.2",
    description="Shuttl Time Library",
    url="",
    author="himaniJoshi",
    author_email="himani.joshi@shuttl.com",
    license="MIT",
    packages=find_packages(),
    classifiers=["Programming Language :: Python :: 3.7"],
    install_requires=["pytz"],
    extras_require={
        "test": ["pytest", "pytest-runner", "pytest-cov", "pytest-pep8"],
        "dev": ["flake8"],
    },
)
