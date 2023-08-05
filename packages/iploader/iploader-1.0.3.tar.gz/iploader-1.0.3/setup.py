import setuptools

#from pip._internal.req import piarse_requirements

#reqs = [str(ir.req) for ir in parse_requirements('requirements.txt', session='hack')]

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="iploader",
    version="1.0.3",
    author="Amir Amiri",
    author_email="Amiri83@gmail.com",
    description="AbuseIPDB Ip Checker",
    scripts= ['bin/iploader',],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Amiri83/IPloader",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
