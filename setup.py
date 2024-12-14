from setuptools import setup, find_packages

setup(
    name="nft-minter",
    version="1.0.0",
    description="A CLI tool for minting, listing, buying, and selling NFTs on Cardano Testnet",
    author="DevBernie",
    author_email="dev.bernie@gmail.com",
    url="https://github.com/devbernie/nft-minter",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    python_requires=">=3.7",
    install_requires=[
        "Click>=8.0",
        "requests>=2.25",
        "pycardano>=0.6.0",
    ],
    entry_points={
        "console_scripts": [
            "nft-minter=cli.cli:cli",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="nft cli cardano blockchain",
    project_urls={
        "Source": "https://github.com/devbernie/nft-minter",
    },
)