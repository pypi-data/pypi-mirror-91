import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="settingsfile", # Replace with your own username
    version="1.0.2",
    author="Ömer Selçuk",
    author_email="omrfyyz@gmail.com",
    description="Memorize settings in Python easily. Autoload and autosave settings to a file.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/divisia/settingsfile",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)