import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="selenium_youtube",
    version="0.3.17",
    author="Kovács Kristóf-Attila & Péntek Zsolt",
    description="selenium_youtube",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kkristof200/selenium_youtube",
    packages=setuptools.find_packages(),
    install_requires=["selenium_firefox", "kstopit", "selenium_uploader_account", "selenium", "kcu", "kyoutubescraper", "beautifulsoup4"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)