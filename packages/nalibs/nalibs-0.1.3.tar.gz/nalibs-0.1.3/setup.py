import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nalibs", # Replace with your own username
    version="0.1.3",
    author="Quang Nguyen",
    author_email="anhquangnet@gmail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "requests",
        "PyYAML"
    ],
    entry_points={
        'console_scripts': [
            'nalibs_hello=nalibs.addfunc:sayHello',
    ],},
    python_requires='>=3.6',
)
