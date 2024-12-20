from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="atlas_hfdatasets",
    version="1.3.9",
    packages=find_packages(),
    install_requires=[
        "huggingface_hub",
        "datasets",
    ],
    author="Haopeng Yu",
    author_email="atlasbioin4@gmail.com",
    description="Manage your datasets on the Hugging Face Hub",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/atlas_hfdatasets",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License", 
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    entry_points={
        'console_scripts': [
            'ahdatasets=atlas_hfdatasets.atlas_hfdatasets:main',
        ],
    },
)