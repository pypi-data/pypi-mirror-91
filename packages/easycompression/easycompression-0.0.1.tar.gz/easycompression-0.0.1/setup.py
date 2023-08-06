import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="easycompression",  # Replace with your own username
    version="0.0.1",
    author="PAI EasyCompression Team",
    author_email="litan.ls@alibaba-inc.com",
    description="Deep learning model compression toolkit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alibaba/EasyCompression",
    packages=setuptools.find_packages(),
    python_requires=">=2.7,>=3.6",
)
