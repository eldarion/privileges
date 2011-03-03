from distutils.core import setup


VERSION = __import__("privileges").__version__


setup(
    name = "privileges",
    version = VERSION,
    author = "Eldarion",
    author_email = "development@eldarion.com",
    description = "an extensible privileges app",
    long_description = open("README.rst").read(),
    license = "BSD",
    url = "http://github.com/eldarion/privileges",
    packages = [
        "privileges",
        "privileges.templatetags",
    ],
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
    ]
)
