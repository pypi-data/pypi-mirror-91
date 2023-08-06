import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    longDesc = fh.read()

requirements = []
with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name = "LyricMasterAPI-LyricScrapping",
    version = "1.0.0",
    author = "proguy914629",
    description = "LyricMaster's API in Python",
    long_description = longDesc,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires='>=3.6'
)
