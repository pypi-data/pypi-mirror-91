import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cgroup-parser", # Replace with your own username
    version="0.0.2",
    author="robertzhu",
    author_email="630268695@qq.com",
    description="cgroup parser for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ZhuYuJin/cgroup-parser",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
