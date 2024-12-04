from setuptools import find_packages, setup

__version__ = "0.1.9"


def _read_long_description():
    try:
        with open("readme.rst") as fd:
            return fd.read()
    except Exception:
        return None


setup(
    name="mailerlite",
    version=__version__,
    author="MailerLite",
    author_email="tech@mailerlite.com",
    url="https://developers.mailerlite.com/",
    description="The official Python SDK for MailerLite API.",
    long_description=_read_long_description(),
    license="MIT",
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries",
    ],
    # Packages and dependencies
    package_dir={"": "src"},
    packages=find_packages("src"),
    install_requires=[],
    extras_require={},
    # Other configurations
    zip_safe=False,
    platforms="any",
)
