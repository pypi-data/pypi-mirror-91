
#!/usr/bin/env python
from setuptools import setup
setup(
    name = "gevent-queue",
    url = "https://github.com/knazarov/gevent-queue",
    description = "A persistent multi-producer multi-consumer gevent queue",
    long_description = "file: README.md",
    version = "0.1.5",
    install_requires=['redis>=3.0.0'],
    license="BSD-3-Clause",
    author="Konstantin Nazarov",
    author_email="mail@knazarov.com",
    py_modules=["gevent_queue"]
)
