import setuptools

with open("README.md", "r", encoding="utf-8") as readme:
    long_description = readme.read()


setuptools.setup(
    name="hastygram",
    version="1.0.0",
    url="https://github.com/zopieux/hastygram",
    author="Alexandre Macabies",
    author_email="web+oss@zopieux.com",
    description="An lightweight frontend for Instagram",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "fastapi~=0.63",
        "aiohttp~=3.7",
    ], classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
)
