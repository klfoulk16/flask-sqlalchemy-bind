import pathlib
import setuptools

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setuptools.setup(
    name="flask-sqlalchemy-bind",
    version="1.0.0",
    description="Minimalistic extension to add support for SQLAlchemy to your Flask app.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/klfoulk16/flask-sqlalchemy-bind",
    author="Kelly Foulk",
    author_email="klf16@my.fsu.edu",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["flask_sqlalchemy_bind"],
    include_package_data=True,
    install_requires=["SQLAlchemy", "Flask"],
)