from setuptools import setup, find_packages

setup(
    name="OblivionCrackerX",
    version="0.1.0",
    author="Jules",
    author_email="",
    description="An advanced, cross-platform decryption tool.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/jules/OblivionCrackerX",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'oblivion=oblivion:main',
        ],
    },
)
