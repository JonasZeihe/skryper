from setuptools import setup, find_packages

setup(
    name="skryper",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[],
    entry_points={
        'console_scripts': [
            'skryper=skryper.main:main',
        ],
    },
    include_package_data=True,
    description="A directory scanning tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/username/skryper",
    author="Jonas Zeihe",
    author_email="jonaszeihe@gmail.com",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
