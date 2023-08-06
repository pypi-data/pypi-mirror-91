DoxyCast
========

.. image:: https://img.shields.io/badge/license-GPLv3-informational
    :alt: License GPLv3

DoxyCast is a documentation generator that helps you to generate beautiful
documentations from the comments you have written in your source code.

DoxyCast reads the XML output from Doxygen and generates reStructuredText
sources, which are parsed by Sphinx to generate the documentations.


Installation
------------

To install DoxyCast, execute the following command::

    pip install doxycast


Getting Started
---------------

Before getting started, make sure you have Doxygen and Sphinx installed. Then
add the following to your ``conf.py``::

    doxycast_config = {
        "projects": {
            "xml_dir": "path/to/xml",
            "output_dir": "path/to/output",
            "execute_doxygen": True,
            "doxycast_config":
                "INPUT = path/to/sources\n"
                # Other Doxygen options

            # "writer": your_custom_writer # Optional, default ``doxycast.writers.default``
        }
    }

Note: if you are using the default writer (not using any custom writer), you
also need to install Breathe.
