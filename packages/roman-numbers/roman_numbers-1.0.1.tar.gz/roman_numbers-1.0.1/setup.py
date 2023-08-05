import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="roman_numbers", # Replace with your own username
    version="1.0.1",
    author="Jirakit Jirapongwanich",
    author_email="jirakit.jpwn@gmail.com",
    description="Convert roman numeral to number and manage roman number object",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)