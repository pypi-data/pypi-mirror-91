from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()


setup(
    install_requires=required,
    name="croudtech-helm-values-parser",  # Replace with your own username
    author="Jim Robinson",
    author_email="jscrobinson@gmail.com",
    description="Helm utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    use_pyscaffold=True,
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
