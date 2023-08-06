import doxycast.config
import doxycast.execute
import doxycast.parser

import os
import sphinx
import sphinx.application

def dump_project(project: str) -> None:
    """
    Writes output.
    """
    if not os.path.isdir(doxycast.config.configuration["projects"][project]["output_dir"]):
        os.mkdir(doxycast.config.configuration["projects"][project]["output_dir"])

    doxycast.config.configuration["projects"][project]["writer"].write_tree(
        project,
        doxycast.config.configuration["projects"][project]["output_dir"],
        doxycast.config.project_roots[project],
        doxycast.config.configuration["projects"][project]["writer_config"],
        doxycast.config.configuration["projects"][project]["xml_dir"]
    )

def dump(app: sphinx.application.Sphinx) -> None:
    """
    Executes Doxygen, parses XML and writes output.
    """

    # Execute Doxygen
    for project in doxycast.config.configuration["projects"]:
        doxycast.execute.execute_doxygen(project)

    print() # Get out of the current line

    # Parse Doxygen output
    for project in doxycast.config.configuration["projects"]:
        doxycast.parser.parse(project)

    print()

    # Optimize the tree
    for project in doxycast.config.configuration["projects"]:
        doxycast.parser.process(project)

    print()

    # Dump data to filesystem
    for project in doxycast.config.configuration["projects"]:
        dump_project(project)

def setup(app: sphinx.application.Sphinx):
    app.connect("builder-inited", dump)
