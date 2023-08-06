from setuptools import setup


with open("README.md", "r") as f:
    desc = f.read()


setup(
    name="cologger",
    version="0.0.1",
    description="Make your endless print statements with color, different formats, and more!",
    py_modules=["cologger"],
    url="https://github.com/henryboisdequin/cologger",
    package_dir={"": "cologger"},
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.9",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
    ],
    long_description=desc,
    long_description_content_type="text/markdown"
)
