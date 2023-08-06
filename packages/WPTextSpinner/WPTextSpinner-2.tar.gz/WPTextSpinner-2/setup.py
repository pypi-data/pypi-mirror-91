import setuptools

setuptools.setup(
    name="WPTextSpinner",
    version="2",
    author="Sascha Huber",
    author_email="kontakt@sascha-huber.com",
    description="Easily spin content for your WP-Sites!",
    long_descritpion="Text-Spinner-Tool for Wordpress",
    long_description_content_type="text/markdown",
    url="https://github.com/dersaschahuber/WPTextSpinner",
    entry_points = {
        'console_scripts': ['WPTextSpinner=WPTextSpinner.CommandLine:main'],
    },
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[]
)