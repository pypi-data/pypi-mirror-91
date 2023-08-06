from setuptools import setup

setup(
    name="Credman",
    version=0.1,
    author="Lightman",
    author_email="L1ghtM3n@protonmail.com",
    description="Python module to retrieve passwords from windows credential manager. (Credman.ReadPasswords())",
    url="https://github.com/L1ghtM4n",
    packages=["Credman"],
    install_requires=[
      ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.8",
)