import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    setuptools.setup(
        name="redditquotebot",
        author="Porthos",
        author_email="etdds@protonmail.com",
        description="Reddit bot for detecting and replying to famous quotes",
        long_description=long_description,
        long_description_content_type="text/markdown",
        packages=setuptools.find_packages(),
        include_package_data=True,
        package_data={
            "redditquotebot": ["data/quotes.csv"]
        },
        classifiers=[
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent"
        ],
        python_requires='>=3.6',
        scripts=[
            "bin/reddit_quote_bot.py",
            "bin/rqb_record_combine.py",
        ],
        install_requires=[
            "praw==7.6.0",
            "spacy==3.4.2"
        ],
        extras_require={},
        use_scm_version=True,
        setup_requires=["setuptools_scm", "wheel"]
    )
