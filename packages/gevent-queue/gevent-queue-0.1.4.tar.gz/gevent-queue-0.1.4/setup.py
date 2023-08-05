import os

from setuptools import setup

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md")) as f:
    long_description = f.read().decode('utf8')

setup(
    name="gevent-queue",
    url="https://github.com/knazarov/gevent-queue",
    description="A persistent multi-producer multi-consumer gevent queue",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version="0.1.4",
    install_requires=["redis>=3.0.0"],
    license="BSD-3-Clause",
    author="Konstantin Nazarov",
    author_email="mail@knazarov.com",
    py_modules=["gevent_queue"],
)
