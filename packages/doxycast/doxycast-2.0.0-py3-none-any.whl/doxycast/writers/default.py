import doxycast.node
import doxycast.utils
from doxycast.utils import ansi_colors

import os
import shutil
import textwrap

def dispatch(project: str, output_dir: str, node: doxycast.node.node, config: dict, xml_dir: str):
    if node.type == "namespace":
        write_namespace(project, output_dir, node, config, xml_dir)
    elif node.type == "class":
        write_class(project, output_dir, node, config, xml_dir)
    elif node.type == "struct":
        write_struct(project, output_dir, node, config, xml_dir)
    elif node.type == "union":
        write_union(project, output_dir, node, config, xml_dir)
    elif node.type == "enum":
        write_enum(project, output_dir, node, config, xml_dir)
    elif node.type == "function":
        write_function(project, output_dir, node, config, xml_dir)
    elif node.type == "variable":
        write_variable(project, output_dir, node, config, xml_dir)
    elif node.type == "typedef":
        write_typedef(project, output_dir, node, config, xml_dir)
    elif node.type == "macro":
        write_macro(project, output_dir, node, config, xml_dir)
    else:
        raise RuntimeError(f"unknown node type: {node.type}")

def output_writing(project: str, file: str) -> None:
    print(
        (' ' * shutil.get_terminal_size().columns) + "\r", # Clean the line
        doxycast.utils.color(ansi_colors.bold) + "doxycast: writing rst: ",
        doxycast.utils.color(ansi_colors.magenta) + project +
        doxycast.utils.color(ansi_colors.bold) + ": " + doxycast.utils.color(ansi_colors.magenta),
        file + doxycast.utils.color(ansi_colors.default),
        sep="",
        end="\r"
    )

def write_namespace(project: str, output_dir: str, node: doxycast.node.node, config: dict, xml_dir: str):
    output_writing(project, os.path.join(output_dir, f"{node.doxygen_id}.rst"))
    file = open(os.path.join(output_dir, f"{node.doxygen_id}.rst"), "w")

    file.write(textwrap.dedent("""
        .. _doxycast_{project}_{doxygen_id}:

        Namespace ``{name}``
        =============={underline}

        .. index:: {name} (C++ namespace)

        *namespace* {name}
        {brief}

        {details}

        .. toctree::
            :caption: Members

    """).format(
        project=project,
        doxygen_id=node.doxygen_id,
        name=node.fully_qualified_name,
        underline="=" * len(node.fully_qualified_name),
        brief=textwrap.indent(node.brief, " " * 4),
        details=textwrap.indent(node.details, " " * 4),
        xml_dir=xml_dir
    ))
    for child in node.children:
        file.write(f"    {child.doxygen_id}\n")

    for child in node.children:
        dispatch(project, output_dir, child, config, xml_dir)

def write_class(project: str, output_dir: str, node: doxycast.node.node, config: dict, xml_dir: str):
    output_writing(project, os.path.join(output_dir, f"{node.doxygen_id}.rst"))
    file = open(os.path.join(output_dir, f"{node.doxygen_id}.rst"), "w")

    file.write(textwrap.dedent("""
        .. _doxycast_{project}_{doxygen_id}:

        Class ``{name}``
        =========={underline}

        .. doxygenclass:: {name}
            :path: {xml_dir}/xml
            :members:
            :protected-members:
    """).format(
        project=project,
        doxygen_id=node.doxygen_id,
        name=node.fully_qualified_name,
        underline="=" * len(node.fully_qualified_name),
        xml_dir=xml_dir
    ))

def write_struct(project: str, output_dir: str, node: doxycast.node.node, config: dict, xml_dir: str):
    output_writing(project, os.path.join(output_dir, f"{node.doxygen_id}.rst"))
    file = open(os.path.join(output_dir, f"{node.doxygen_id}.rst"), "w")

    file.write(textwrap.dedent("""
        .. _doxycast_{project}_{doxygen_id}:

        Struct ``{name}``
        ==========={underline}

        .. doxygenstruct:: {name}
            :path: {xml_dir}/xml
            :members:
            :protected-members:
    """).format(
        project=project,
        doxygen_id=node.doxygen_id,
        name=node.fully_qualified_name,
        underline="=" * len(node.fully_qualified_name),
        xml_dir=xml_dir
    ))

def write_union(project: str, output_dir: str, node: doxycast.node.node, config: dict, xml_dir: str):
    output_writing(project, os.path.join(output_dir, f"{node.doxygen_id}.rst"))
    file = open(os.path.join(output_dir, f"{node.doxygen_id}.rst"), "w")

    file.write(textwrap.dedent("""
        .. _doxycast_{project}_{doxygen_id}:

        Union ``{name}``
        =========={underline}

        .. doxygenunion:: {name}
            :path: {xml_dir}/xml
    """).format(
        project=project,
        doxygen_id=node.doxygen_id,
        name=node.fully_qualified_name,
        underline="=" * len(node.fully_qualified_name),
        xml_dir=xml_dir
    ))

def write_enum(project: str, output_dir: str, node: doxycast.node.node, config: dict, xml_dir: str):
    output_writing(project, os.path.join(output_dir, f"{node.doxygen_id}.rst"))
    file = open(os.path.join(output_dir, f"{node.doxygen_id}.rst"), "w")

    file.write(textwrap.dedent("""
        .. _doxycast_{project}_{doxygen_id}:

        Enum ``{name}``
        ========={underline}

        .. doxygenenum:: {name}
            :path: {xml_dir}/xml
    """).format(
        project=project,
        doxygen_id=node.doxygen_id,
        name=node.fully_qualified_name,
        underline="=" * len(node.fully_qualified_name),
        xml_dir=xml_dir
    ))

def write_function(project: str, output_dir: str, node: doxycast.node.node, config: dict, xml_dir: str):
    output_writing(project, os.path.join(output_dir, f"{node.doxygen_id}.rst"))
    file = open(os.path.join(output_dir, f"{node.doxygen_id}.rst"), "w")

    file.write(textwrap.dedent("""
        .. _doxycast_{project}_{doxygen_id}:

        Function ``{name}``
        ============={underline}

        .. doxygenfunction:: {name}
            :path: {xml_dir}/xml
    """).format(
        project=project,
        doxygen_id=node.doxygen_id,
        name=node.fully_qualified_name,
        underline="=" * len(node.fully_qualified_name),
        xml_dir=xml_dir
    ))

def write_variable(project: str, output_dir: str, node: doxycast.node.node, config: dict, xml_dir: str):
    output_writing(project, os.path.join(output_dir, f"{node.doxygen_id}.rst"))
    file = open(os.path.join(output_dir, f"{node.doxygen_id}.rst"), "w")

    file.write(textwrap.dedent("""
        .. _doxycast_{project}_{doxygen_id}:

        Variable ``{name}``
        ============={underline}

        .. doxygenvariable:: {name}
            :path: {xml_dir}/xml
    """).format(
        project=project,
        doxygen_id=node.doxygen_id,
        name=node.fully_qualified_name,
        underline="=" * len(node.fully_qualified_name),
        xml_dir=xml_dir
    ))

def write_typedef(project: str, output_dir: str, node: doxycast.node.node, config: dict, xml_dir: str):
    output_writing(project, os.path.join(output_dir, f"{node.doxygen_id}.rst"))
    file = open(os.path.join(output_dir, f"{node.doxygen_id}.rst"), "w")

    file.write(textwrap.dedent("""
        .. _doxycast_{project}_{doxygen_id}:

        Typedef ``{name}``
        ============{underline}

        .. doxygentypedef:: {name}
            :path: {xml_dir}/xml
    """).format(
        project=project,
        doxygen_id=node.doxygen_id,
        name=node.fully_qualified_name,
        underline="=" * len(node.fully_qualified_name),
        xml_dir=xml_dir
    ))

def write_macro(project: str, output_dir: str, node: doxycast.node.node, config: dict, xml_dir: str):
    output_writing(project, f"{node.doxygen_id}.rst")
    file = open(os.path.join(output_dir, f"{node.doxygen_id}.rst"), "w")

    file.write(textwrap.dedent("""
        .. _doxycast_{project}_{doxygen_id}:

        Macro ``{name}``
        =========={underline}

        .. doxygendefine:: {name}
            :path: {xml_dir}/xml
    """).format(
        project=project,
        doxygen_id=node.doxygen_id,
        name=node.fully_qualified_name,
        underline="=" * len(node.fully_qualified_name),
        xml_dir=xml_dir
    ))

def write_tree(project: str, output_dir: str, node: doxycast.node.node, config: dict, xml_dir: str) -> None:
    output_writing(project, os.path.join(output_dir, "index.rst"))
    file = open(os.path.join(output_dir, "index.rst"), "w")

    file.write(textwrap.dedent("""
        API Documentation
        =================

        .. **Symbol hierarchy**:

        .. toctree::
            :caption: Symbol hierarchy
            :maxdepth: -1

    """))

    for child in node.child("global-namespace").children:
        file.write(f"    {child.doxygen_id}\n")

    for child in node.child("global-namespace").children:
        dispatch(project, output_dir, child, config, xml_dir)

    print() # Get out of the current line

def setup(app) -> None:
    pass
