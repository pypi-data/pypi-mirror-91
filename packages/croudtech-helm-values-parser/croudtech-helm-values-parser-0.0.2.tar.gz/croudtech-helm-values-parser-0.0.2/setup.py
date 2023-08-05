from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    install_requires=find_packages(),
    name="croudtech-helm-values-parser",  # Replace with your own username
    version="0.0.2",
    author="Jim Robinson",
    author_email="jscrobinson@gmail.com",
    description="Helm utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CroudTech/devops-python-package-deployment-worker",
    packages=["croudtech_helm_values_parser"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "croudtech-helm-values-parser=croudtech_helm_values_parser.cli:cli"
        ],
    },
)
