import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wiserHeatAPIv2", # Replace with your own username
    version="0.0.2",
    author="Mark Parker",
    author_email="msparker@sky.com",
    description="An API for controlling the Drayton Wiser Heating system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/msp1974/wiserheatapiv2",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
