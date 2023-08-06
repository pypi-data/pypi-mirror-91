import setuptools
import os

os.system("export PATH=$PATH:~/.local/bin")

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kubextract",
    version="1.1.4",
    author="Bentar Dwika",
    author_email="bentar@warungpintar.co",
    description="cli framework generator for developing ML on kubeflow",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={
        "kubextract": ["params/*", "templates/*"]
    },
    install_requires=[
        'kubernetes==11.0.0',
        'ruamel.yaml==0.16.10',
        'click==7.1.2',
        'PyInquirer==1.0.3',
        'prompt_toolkit==1.0.14',
        'urllib3==1.25.9',
        'requests==2.23.0',
        'kfp==1.2.0'
    ],
    entry_points={
        'console_scripts': [
            'kubextract = kubextract.utils.generate:main',
            'pipeline = kubextract.utils.pipeline:main'
        ],
    },
    python_requires='>=3.6',
)
