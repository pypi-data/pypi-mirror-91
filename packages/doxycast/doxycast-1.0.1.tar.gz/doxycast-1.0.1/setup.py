import setuptools

setuptools.setup(
    name="doxycast",
    version="1.0.1",
    description="Generate reStructuredText documentations from your C++ sources",
    long_description=open("README.rst", "r").read(),
    long_description_content_type="text/x-rst",
    url="https://gitlab.com/pypp/doxycast",
    author="Akib Azmain",
    author_email="akib8492@gmail.com",
    license="GNU Lesser General Public License v3 or later (LGPLv3+)",
    classifiers=[
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Framework :: Sphinx",
        "Framework :: Sphinx :: Extension",
        "Intended Audience :: Developers",
        "Development Status :: 4 - Beta",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Documentation",
        "Topic :: Documentation :: Sphinx",
        "Topic :: Software Development :: Documentation"
    ],
    packages=[
        "doxycast",
        "doxycast.writers"
    ],
    install_requires=[
        "sphinx"
    ],
    extras_require={
        "Default writer": "breathe"
    }
)
