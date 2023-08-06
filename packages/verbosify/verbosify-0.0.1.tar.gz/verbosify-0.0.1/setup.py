from setuptools import setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='verbosify',
    version='0.0.1',
    description="A cool python function decorator to print comments",
    packages=['verbosify'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rhuille/verbosify",
    author='Raphael Huille',
    author_email='raphael.huille@gmail.com',
    license='MIT',
    python_requires='>=3.8',
)
