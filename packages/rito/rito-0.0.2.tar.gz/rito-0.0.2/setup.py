import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rito",
    version="0.0.2",
    author="Nat Quayle Nelson",
    author_email="natquaylenelson@gmail.com",
    description="Very simple ways to send notifications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NQNStudios/rito",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests',
        'click',
        'markdown'
    ],
    entry_points='''
        [console_scripts]
        rito=rito.cli:cli
    ''',
)