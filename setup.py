import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    setuptools.setup(
        name="redditquotebot",
        author="Porthos",
        author_email="stuian@protonmail.com",
        description="Reddit bot for detecting and replying to famous quotes",
        long_description=long_description,
        long_description_content_type="text/markdown",
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent"
        ],
        python_requires='>=3.6',
        install_requires=["praw==7.6.0"],
        extras_require={},
    )
