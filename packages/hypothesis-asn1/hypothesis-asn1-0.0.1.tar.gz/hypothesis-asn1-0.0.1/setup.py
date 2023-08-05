import os

import setuptools


def local_file(name: str) -> str:
    """Interpret filename as relative to this file."""
    return os.path.relpath(os.path.join(os.path.dirname(__file__), name))


SOURCE = local_file("src")
README = local_file("README.md")

with open(local_file("src/hypothesis_asn1/__init__.py")) as o:
    for line in o:
        if line.startswith("__version__"):
            _, __version__, _ = line.split('"')


setuptools.setup(
    name="hypothesis-asn1",
    version=__version__,
    author="Zac Hatfield-Dodds",
    author_email="zac@zhd.dev",
    packages=setuptools.find_packages(SOURCE),
    package_dir={"": SOURCE},
    package_data={"": ["py.typed"]},
    url="https://github.com/Zac-HD/hypothesis-asn1",
    license="MPL 2.0",
    description="Generate test data from ASN.1 descriptions with Hypothesis",
    zip_safe=False,
    install_requires=["hypothesis>=6.0.0", "pyasn1>=0.4.8"],
    python_requires=">=3.6",
    classifiers=[
        # See https://pypi.org/classifiers/
        "Development Status :: 1 - Planning",
        "Framework :: Hypothesis",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Testing",
        "Typing :: Typed",
    ],
    long_description=open(README).read(),
    long_description_content_type="text/markdown",
    keywords="python testing fuzzing property-based-testing ASN.1",
)
