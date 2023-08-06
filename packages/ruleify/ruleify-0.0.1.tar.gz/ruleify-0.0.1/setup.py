import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ruleify",
    version="0.0.1",
    author="Unai Ltd",
    author_email="ruleify@unai.com",
    description="A python rules engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/unai/ruleify",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
