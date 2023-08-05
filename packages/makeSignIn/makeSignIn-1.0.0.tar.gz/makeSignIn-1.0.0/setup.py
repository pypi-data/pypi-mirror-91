from setuptools import setup
__project__ = "makeSignIn"
__version__ = "1.0.0"
__description__ = "a Python module to create a sign in page for your python project."
__packages__ = ["makesignin"]
__author__ = "Viraj Khanna"
__author_email__ = "virajkhanna2811@gmail.com"
__classifiers__ = ["Development Status :: 5 - Production/Stable", "Intended Audience :: Developers", "License :: OSI Approved :: Boost Software License 1.0 (BSL-1.0)","Programming Language :: Python :: 3.9", "Natural Language :: English", "Topic :: Software Development :: Libraries", "Typing :: Typed"]
setup(
    name = __project__,
    version = __version__,
    description = __description__,
    packages = __packages__,
    author = __author__,
    author_email = __author_email__,
    install_requires=[
        "win10toast",
        "getpass",
    ],
    classifiers = __classifiers__,
)
