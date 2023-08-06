import setuptools


with open("discordpython/README.md","r",encoding="utf-8") as fhandle:
  long_description=fhandle.read()

setuptools.setup(
    name="discordpython", #Package Name!
    version="0.0.2", # The version of your package!
    author="DiscordDev", # Your name here!
    author_email="example@example.com", # Your e-mail here!
    description="Python cog discord.py", # A short description here!
    long_description=long_description,
    long_description_content_type="text/markdown",
    requirement=["humanize>=3.8.0"],
    url="https://github.com", # Link your package website here! (most commonly a GitHub repo)
    packages=setuptools.find_packages(), # A list of all packages for Python to distribute!
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ], # Enter meta data into the classifiers list!
    python_requires='>=3.6', # The version requirement for Python to run your package!
)
