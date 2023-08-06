"""
The module responsible for handling configuration.

This modules handles all configurations.
"""

from doxycast.node import node

import textwrap
import sphinx
import sphinx.application
import sphinx.errors

configuration = dict()
"""
The configuration of DoxyCast. This dictionary has the following structure::

    doxycast_config = {

        "projects": {

            "my_lib": {

                "xml_dir": "path/to/xml/directory",             # str

                "output_dir": "path/to/output/directory",       # str

                "execute_doxygen": True,                        # bool

                "doxygen_config": "...",                        # str
                    # Required if "execute_doxygen" is True and "doxygen_config_file" not specified

                "doxygen_config_file": "path/to/doxyfile",      # str
                    # Required if "execute_doxygen" is true and "doxygen_config" not specified, not
                    # used if "doxygen_config" specified

                "doxygen_verbose": True,                        # bool
                    # Optional, default "True", can't be specified when "execute_doxygen" is False

                "doxygen_warning": True,                        # bool
                    # Optional, default "True", can't be specified when "execute_doxygen" is False

                "doxygen_warnings_prettify": True,              # bool
                    # Optional, default "True", can't be specified when either "execute_doxygen" or
                    # or "doxygen_warning" is False

                "debug": True,                                  # bool
                    # Optional, default "False"

                "writer": ...                                   # module
                    # Optional, default is "doxycast.writers.default"

                "writer_config": {...}                          # dict
                    # Optional, default is an empty dictionary

                "fixes": [...]                                  # list
                    # Optional, applies various fixes and patches on Doxygen
                    # XML. Invalid values doesn't show any warnings. Possible
                    # options:
                    #
                    # * ``misinterpreted_typedef_0``: Fixes typedef
                    #   misinterpreted as variable

            },

            # More with same structure...
        },

        "default_project": "..."                                # str
            # Optional, default is None, the default project

        # Some more global config
    }
"""

default_project = None
"""
The default project.
"""

project_roots = dict()

def setup_project(app: sphinx.application.Sphinx, project: str) -> None:
    """
    Setups a project.
    """

    # Make sure the project configuration is a dictionary
    if type(configuration["projects"][project]) is not dict:
        raise sphinx.errors.ConfigError(textwrap.dedent("""
            project configurations in \"doxycast_config\" must be defined as \"dict\"
        """)[1:-1]) # Strip leading and trailing newline

    error_message = "\"{key}\" in project configurations must be \"{value_t}\""

    # Check value types
    if type(configuration["projects"][project].get("xml_dir", None)) is not str:
        raise sphinx.errors.ConfigError(error_message.format(key="xml_dir", value_t="str"))

    if type(configuration["projects"][project].get("output_dir", None)) is not str:
        raise sphinx.errors.ConfigError(error_message.format(key="output_dir", value_t="str"))

    if type(configuration["projects"][project].get("execute_doxygen", None)) is not bool:
        raise sphinx.errors.ConfigError(error_message.format(key="execute_doxygen", value_t="bool"))
    else:

        # Make sure required keys are defined with correct type if "execute_doxygen" is True
        if configuration["projects"][project]["execute_doxygen"]:
            if (
                type(configuration["projects"][project].get("doxygen_config", None)) is not str and
                type(configuration["projects"][project].get("doxygen_config_file", None)) is not str
            ):
                raise sphinx.errors.ConfigError(
                    "either \"doxygen_config\" or \"doxygen_config_file\" must be defined when " +
                    "\"execute_doxygen\" is \"True\""
                )

    # Check whether optional keys are defined,
    #   check whether they are defined with correct type,
    # otherwise set default value
    if configuration["projects"][project].get("doxygen_verbose", None) != None:
        if type(configuration["projects"][project]["doxygen_verbose"]) is not bool:
            raise sphinx.errors.ConfigError(error_message.format(key="doxygen_verbose", type="bool"))
    else:
        configuration["projects"][project]["doxygen_verbose"] = True

    if configuration["projects"][project].get("doxygen_warning", None) != None:
        if type(configuration["projects"][project]["doxygen_warning"]) is not bool:
            raise sphinx.errors.ConfigError(error_message.format(key="doxygen_warning", type="bool"))
    else:
        configuration["projects"][project]["doxygen_warning"] = True

    if configuration["projects"][project].get("doxygen_warnings_prettify", None) != None:
        if type(configuration["projects"][project]["doxygen_warnings_prettify"]) is not bool:
            raise sphinx.errors.ConfigError(
                error_message.format(key="doxygen_warnings_prettify", type="bool")
            )
    else:
        configuration["projects"][project]["doxygen_warnings_prettify"] = True

    if configuration["projects"][project].get("debug", None) != None:
        if type(configuration["projects"][project]["debug"]) is not bool:
            raise sphinx.errors.ConfigError(error_message.format(key="debug", type="bool"))
    else:
        configuration["projects"][project]["debug"] = True

    if configuration["projects"][project].get("writer", None) == None:
        import doxycast.writers.default
        configuration["projects"][project]["writer"] = doxycast.writers.default

    if configuration["projects"][project].get("writer_config", None) != None:
        if type(configuration["projects"][project]["writer_config"]) is not bool:
            raise sphinx.errors.ConfigError(error_message.format(key="writer_config", type="bool"))
    else:
        configuration["projects"][project]["writer_config"] = dict()

    if configuration["projects"][project].get("fixes", None) != None:
        if type(configuration["projects"][project]["fixes"]) is not list:
            raise sphinx.errors.ConfigError(error_message.format(key="fixes", type="bool"))
    else:
        configuration["projects"][project]["fixes"] = list()

    global project_roots
    project_roots[project] = node(
        type="root",
        name="root",
        definition="root",
        doxygen_id="root",
        parent=None,
        children=[],
        brief="Project root node",
        details=textwrap.dedent("""
            The root node of the project. This node is a special type of node,
            with all other nodes within same project referenced hierarchically.
            Documentation for this node should never be generated.
        """)
    )

    configuration["projects"][project]["writer"].setup(app)

def setup_config(app: sphinx.application.Sphinx, conf) -> None:
    """
    Setups configuration and projects.
    """
    global configuration

    try:
        configuration = conf.doxycast_config
    except:
        raise sphinx.errors.ConfigError("\"doxycast_config\" must be defined in \"conf.py\"")

    # Make sure "doxycast_config" is a list
    if type(configuration) is not dict:
        raise sphinx.errors.ConfigError("\"doxycast_config\" must be a \"dict\"")

    # Make sure "doxycast_config" has at least one project
    if type(configuration.get("projects", None)) is not dict or len(configuration["projects"]) == 0:
        raise sphinx.errors.ConfigError("\"doxycast_config\" must have at least one project")

    # Set the default project
    global default_project
    default_project = configuration.get("default_project", None)

    # Setup each project
    for project in configuration["projects"]:
        setup_project(app, project)

def setup(app: sphinx.application.Sphinx):
    app.add_config_value("doxycast_config", dict(), "env")
    app.connect("config-inited", setup_config)
