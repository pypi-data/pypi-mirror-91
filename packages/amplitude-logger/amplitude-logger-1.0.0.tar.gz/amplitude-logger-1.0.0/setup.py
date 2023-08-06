
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="amplitude-logger",
    version="1.0.0",
    author="Serhii Zahranychnyi",
    author_email="zagranlab@gmail.com",
    description="Amplitude API v2 logger for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zagran/amplitude-logger",
    packages=setuptools.find_packages(),
    install_requires=["requests==2.22.0", ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)