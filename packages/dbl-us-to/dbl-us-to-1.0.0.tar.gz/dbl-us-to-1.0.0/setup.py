import setuptools


with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()

with open("requirements.txt", "r") as file:
    requirements = file.readlines()

setuptools.setup(
    name="dbl-us-to",
    version="1.0.0",
    author="MrSpinne",
    author_email="spinningplays.gaming@gmail.com",
    description="An API wrapper for discordbotslist.us.to written in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MrSpinne/DiscordBotsList.py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="discordbotslist, api, wrapper, botlist, stats, discord.py",
    python_requires='>=3.7',
    install_requires=requirements
)
