import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="bitbitbot",
    version="0.0.1",
    author="William Johns",
    author_email="will@wcj.dev",
    description="An unopionated, extensible Twitch Chat Bot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MetaBytez/bitbitbot",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    install_requires=[
        'irc==19.0.1',
        'pydantic==1.7.3'
    ]
)
