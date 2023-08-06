import doxycast.config
import doxycast.node
import doxycast.utils
from doxycast.utils import ansi_colors

import os
import re
import shutil
import textwrap
import xml.etree.ElementTree
import xml.dom.minidom

compound_roots = dict()

def output_reading_xml(project: str, file: str):
    """
    Prints the message ``reading xml: {project}: {file}``
    """
    print(
        (' ' * shutil.get_terminal_size().columns) + "\r", # Clean the line
        doxycast.utils.color(ansi_colors.bold) + "doxycast: reading xml: ",
        doxycast.utils.color(ansi_colors.magenta) + project +
        doxycast.utils.color(ansi_colors.bold) + ": " + doxycast.utils.color(ansi_colors.magenta),
        file + doxycast.utils.color(ansi_colors.default),
        sep="",
        end="\r"
    )

def get_metadata(project: str, node: xml.dom.minidom.Element, metadata: dict) -> dict:
    """
    Return a dictionary holding information about parameters, template
    parameters, return, author, etc.
    """
    for child in node.childNodes:

        # Make sure the child is an element node
        if child.nodeType == xml.dom.minidom.Node.ELEMENT_NODE:

            # Check if the node holds (template) paramters
            if child.tagName == "parameterlist":
                param_type = child.getAttribute("kind")
                metadata[param_type] = dict()

                for item in child.childNodes:
                    if item.nodeType == xml.dom.minidom.Node.ELEMENT_NODE:
                        metadata[param_type][get_text(project, item.getElementsByTagName("parametername")[0])[0]] \
                            = get_text(project, item.getElementsByTagName("parameterdescription")[0])[0]

            # Check if node holds return, author, etc
            if child.tagName == "simplesect":
                metadata[child.getAttribute("kind")] = get_text(project, child)[0]

    return metadata

def get_attributes(attributes: str):
    """
    Returns a dictionary of attributes of the node.
    """
    temp_attributes = textwrap.dedent(attributes)
    attributes = str()

    # Remove escaped newlines
    escape = False
    for character in temp_attributes:
        if escape:
            if character == "\\":
                attributes += "\\"

            escape = False
            continue

        if character == "\\":
            escape = True
        else:
            attributes += character

    attributes = attributes.splitlines()

    attributes_list = list()

    for attribute in attributes:
        if not attribute:
            continue
        attributes_list.append(attribute.split(" ", 1))

    return attributes_list

def get_text(project: str, node: xml.dom.minidom.Node) -> list:
    """
    Returns reStructureText from XML encoded text.
    """
    rst_src: str                = str()
    metadata: dict              = dict()

    iterate_children            = True

    paragraph                   = False
    verbatim_leading_asterisks  = False
    computer_output             = False
    formula                     = False
    reference                   = False

    if node.nodeType == xml.dom.minidom.Node.ELEMENT_NODE:
        paragraph                       = node.tagName == "para"
        verbatim_leading_asterisks      = (
            node.tagName == "verbatim" and
            node.childNodes[0].data.startswith("embed:rst:leading-asterisk")
        )
        attributes                      = (
            node.tagName == "verbatim" and
            node.childNodes[0].data.startswith("attributes")
        )
        attributes_leading_asterisks    = (
            node.tagName == "verbatim" and
            node.childNodes[0].data.startswith("attributes:leading-asterisk")
        )
        computer_output                 = node.tagName == "computeroutput"
        formula                         = node.tagName == "formula"
        bold                            = node.tagName == "bold"
        emphasis                        = node.tagName == "emphasis"
        reference                       = node.tagName == "ref"

        if node.tagName == "sp":
            return " " # SPACE


    elif node.nodeType == xml.dom.minidom.Node.TEXT_NODE:
        return (node.data if not node.data.isspace() else str()), metadata

    # If iterate_children is True, iterate over children
    if iterate_children:
        for child in node.childNodes:

            # Check if it is a special "para" with "param"s
            if (
                node.nodeType == xml.dom.minidom.Node.ELEMENT_NODE and
                node.tagName == "detaileddescription" and
                child.nodeType == xml.dom.minidom.Node.ELEMENT_NODE and
                child.tagName == "para" and
                (
                    len(child.getElementsByTagName("parameterlist")) != 0 or
                    len(child.getElementsByTagName("simplesect")) != 0
                )
            ):
                metadata = get_metadata(project, child, metadata)

            if not (
                node.nodeType == xml.dom.minidom.Node.ELEMENT_NODE and
                node.tagName == "detaileddescription" and
                child == xml.dom.minidom.Node.TEXT_NODE
            ) and not (
                child.nodeType == xml.dom.minidom.Node.ELEMENT_NODE and
                child.tagName in ["parameterlist", "simplesect"]
            ):
                data = get_text(project, child)
                rst_src += data[0]
                metadata = {**metadata, **data[1]}

    if attributes_leading_asterisks:
        return (
            str(),
            {
                "attributes":
                    get_attributes(
                        textwrap.dedent(rst_src[27:].replace("\n*", "\n")[1:-1])
                    )
            }
        )
    elif attributes:
        return (
            str(),
            {
                "attributes":
                    get_attributes(rst_src[11:])
            }
        )
    elif paragraph:
        rst_src = f"\n\n{rst_src}\n\n"
    elif verbatim_leading_asterisks:
        rst_src = textwrap.dedent(rst_src[26:].replace("\n*", "\n")[1:-1])
    elif bold:
        rst_src = f"**{rst_src}**"
    elif emphasis:
        rst_src = f"*{rst_src}*"
    elif computer_output:
        rst_src = f"``{rst_src}``"
    elif formula:
        rst_src = f":math:`{rst_src[1:-1]}`"
    elif reference:
        rst_src = f":ref:`{rst_src} <doxycast_{project}_{node.getAttribute('refid')}>`"

    return rst_src, metadata

def process_graph(node: xml.dom.minidom.Element) -> list:
    """
    Return a list of nodes from graph definitions in XML.
    """
    nodes = dict()
    for relation in node.childNodes:
        if (
            relation.nodeType == xml.dom.minidom.Node.ELEMENT_NODE and
            relation.tagName == "node"
        ):
            id = int(relation.getAttribute("id"))

            try:
                label: str = relation.getElementsByTagName("label")[0].childNodes[0].data
            except IndexError:
                label = str()

            try:
                refid: str = relation.getElementsByTagName("link")[0].getAttribute("refid")
            except IndexError:
                refid = None

            children: list = list()

            for child in relation.getElementsByTagName("childnode"):
                child_refid = int(child.getAttribute("refid"))
                relation_type = child.getAttribute("relation")

                try:
                    extra_modifiers = [child_node.childNodes[0].data for child_node in child.childNodes]
                except IndexError:
                    extra_modifiers = []

                children.append([child_refid, relation_type, extra_modifiers])

            nodes[id] = doxycast.node.graph_node(label, refid, children)

    return nodes

def process_memberdef(project: str, memberdef: xml.dom.minidom.Element, parent: doxycast.node.node):
    """
    Returns the definitions of a member from XML.
    """
    member_node: doxycast.node.node = doxycast.node.node(
        doxygen_id=memberdef.getAttribute("id"),
        type=memberdef.getAttribute("kind"),
        parent=parent,
        children=[],
        name=memberdef.getElementsByTagName("name")[0].childNodes[0].nodeValue
    )
    parent.children.append(member_node)

    if len(memberdef.getElementsByTagName("definition")) != 0:
        member_node.definition = re.sub(r":ref:`(.*?)(\s*<.*?>)`", r"\1",
            get_text(project, memberdef.getElementsByTagName("definition")[0])[0]
        )

    if member_node.type == "function":
        member_node.const_qualified = memberdef.getAttribute("const") == "yes"
        member_node.definition += re.sub(r":ref:`(.*?)(\s*<.*?>)`", r"\1",
            get_text(project, memberdef.getElementsByTagName("argsstring")[0])[0]
        )

    elif member_node.type == "enum":
        if len(memberdef.getElementsByTagName("type")) != 0:
            member_node.value_type = \
                get_text(project, memberdef.getElementsByTagName("type")[0])[0]
        else:
            member_node.value_type = None

    for node in memberdef.childNodes:

        # Skip non-Element nodes
        if node.nodeType != xml.dom.minidom.Node.ELEMENT_NODE:
            continue

        # Check if current node is brief description
        if node.tagName == "briefdescription":
            member_node.brief = get_text(project, node)[0]

        # Check if current node is detailed description
        elif node.tagName == "detaileddescription":
            member_node.details, member_node.metadata = get_text(project, node)

        # Check if node representing template parameters
        elif node.tagName == "templateparamlist":
            member_node.template_parameters = \
                member_node.__dict__.get("template_parameters", list())
            for param in node.getElementsByTagName("param"):
                parameter = {
                    "type": get_text(project, param.getElementsByTagName("type")[0])[0]
                }
                if len(param.getElementsByTagName("defval")) != 0:
                    parameter["default"] = \
                        get_text(project, param.getElementsByTagName("defval")[0])[0]
                member_node.template_parameters.append(parameter)

        # Check if current node representing parameter
        elif node.tagName == "param":
            member_node.parameters = member_node.__dict__.get("parameters", list())
            parameter = {
                "type": get_text(project, node.getElementsByTagName("type")[0])[0]
            }
            if len(node.getElementsByTagName("defval")) != 0:
                parameter["default"] = \
                    get_text(project, node.getElementsByTagName("defval")[0])[0]
            if len(node.getElementsByTagName("declname")) != 0:
                parameter["name"] = \
                    get_text(project, node.getElementsByTagName("declname")[0])[0]
            member_node.parameters.append(parameter)

        # Check if current node representing enum value
        elif node.tagName == "enumvalue":
            member_node.values = member_node.__dict__.get("values", list())
            value = {
                "name": get_text(project, node.getElementsByTagName("name")[0])[0]
            }
            if len(node.getElementsByTagName("briefdescription")) != 0:
                value["brief"] = \
                    get_text(project, node.getElementsByTagName("briefdescription")[0])[0]
            if len(node.getElementsByTagName("detaileddescription")) != 0:
                value["details"] = \
                    get_text(project, node.getElementsByTagName("detaileddescription")[0])[0]
            if len(node.getElementsByTagName("initializer")) != 0:
                value["value"] = \
                    get_text(project, node.getElementsByTagName("initializer")[0])[0][2:]
            member_node.values.append(value)

        # Check if current node is pointing to source
        elif node.tagName == "location":
            member_node.defined_at = \
                f"{node.getAttribute('file')}:{node.getAttribute('line')}:{node.getAttribute('column')}"

def process_compound(project: str, refid: str) -> doxycast.node.node:
    """
    Returns the definitions of a compound from XML.
    """
    global compound_roots
    if compound_roots[project].get(refid, None) != None:
        return compound_roots[project][refid]

    compound_file: str = os.path.join(
        doxycast.config.configuration["projects"][project]["xml_dir"], "xml", f"{refid}.xml"
    )

    # Output progress
    output_reading_xml(project, compound_file)

    # Open and parse the file
    definition: xml.dom.minidom.Element = xml.dom.minidom.parse(
        compound_file
    ).documentElement.getElementsByTagName("compounddef")[0]

    compound_node: doxycast.node.node = doxycast.node.node(
        doxygen_id=definition.getAttribute("id"),
        type=definition.getAttribute("kind"),
        parent=doxycast.config.project_roots[project],
        children=[],
        name=definition.getElementsByTagName("compoundname")[0].childNodes[0].nodeValue
    )
    doxycast.config.project_roots[project].children.append(compound_node)

    for node in definition.childNodes:

        # Skip non-Element nodes
        if node.nodeType != xml.dom.minidom.Node.ELEMENT_NODE:
            continue

        # Check if current node is brief description
        if node.tagName == "briefdescription":
            compound_node.brief = get_text(project, node)[0]

        # Check if current node is detailed description
        elif node.tagName == "detaileddescription":
            compound_node.details, compound_node.metadata = get_text(project, node)

        # Check if current node is refering to a base
        elif node.tagName == "basecompoundref":
            compound_node.bases = compound_node.__dict__.get("bases", list())
            if node.getAttribute("refid") != str():
                compound_node.bases.append(node.getAttribute("refid"))

        # Check if current node is refering to a derived
        elif node.tagName == "derivedcompoundref":
            compound_node.derived = compound_node.__dict__.get("derived", list())
            if node.getAttribute("refid") != str():
                compound_node.derived.append(node.getAttribute("refid"))

        # Check if node has definitions of a member symbols
        elif node.tagName == "sectiondef":
            for memberdef in node.getElementsByTagName("memberdef"):
                process_memberdef(project, memberdef, compound_node)

        # Check if node has definitions of a graph
        elif node.tagName == "inheritancegraph":
            compound_node.inheritance_graph = process_graph(node)

        # Check if node has definitions of a graph
        elif node.tagName == "collaborationgraph":
            compound_node.collaboration_graph = process_graph(node)

        # Check if node representing template parameters
        elif node.tagName == "templateparamlist":
            compound_node.template_parameters = \
                compound_node.__dict__.get("template_parameters", list())
            for param in node.getElementsByTagName("param"):
                parameter = {
                    "type": get_text(project, param.getElementsByTagName("type")[0])[0]
                }
                if len(node.getElementsByTagName("defval")) != 0:
                    parameter["default"] = \
                        get_text(project, node.getElementsByTagName("defval")[0])[0]
                compound_node.template_parameters.append(parameter)

        # Check if current node is pointing to source
        elif node.tagName == "location":
            compound_node.defined_at = \
                f"{node.getAttribute('file')}:{node.getAttribute('line')}:{node.getAttribute('column')}"

        # Check if current node is **crossrefering** a children
        elif node.tagName[:5] == "inner" and compound_node.type != "file":
            process_compound(project, node.getAttribute("refid")).reparent(compound_node)

    compound_roots[project][refid] = compound_node
    return compound_node

def parse(project: str):
    """
    Processes the index file and other files referred.
    """
    index_file: str = os.path.join(
        doxycast.config.configuration["projects"][project]["xml_dir"], "xml", "index.xml"
    )

    # Output progress
    output_reading_xml(project, index_file)

    # Parse the index
    index: xml.etree.ElementTree.Element = xml.etree.ElementTree.parse(index_file).getroot()
        # Possible question: Why use ElementTree here where DOM is used in other parts?
        # Answer: It's enough here. Is there any need to break a butterfly upon a wheel?

    # Parse all compounds
    global compound_roots
    compound_roots[project] = dict()
    for compound in index:
        process_compound(project, compound.attrib["refid"])

def process(project: str):
    """
    Optimizes and post-processes all nodes.
    """
    print(
        (' ' * shutil.get_terminal_size().columns) + "\r", # Clean the line
        doxycast.utils.color(ansi_colors.bold) + "doxycast: processing: ",
        doxycast.utils.color(ansi_colors.magenta) + project +
        doxycast.utils.color(ansi_colors.default),
        sep="",
        end="\r"
    )

    global_namespace = doxycast.node.node(
        type="namespace",
        name=":: <global namespace>",
        definition="namespace ::",
        doxygen_id="global-namespace",
        parent=doxycast.config.project_roots[project],
        children=[],
        brief="Global namespace",
        details=textwrap.dedent("""
            The global namespace of the project. This node is a special type of
            node, with all other symbol nodes (e.g functions, classes, but not
            directories and files) within same the project referenced
            hierarchically. Documentation for this node should never be
            generated.
        """)
    )

    root_directory = doxycast.node.node(
        type="dir",
        name="/ <root>",
        definition="directory /",
        doxygen_id="root-directory",
        parent=doxycast.config.project_roots[project],
        children=[],
        brief="Root directory",
        details=textwrap.dedent("""
            The filesystem root of the project. This node is a special type of
            node, with all other nodes representing directories and files within
            the same project referenced hierarchically. Documentation for this
            node should never be generated.
        """)
    )

    groups = doxycast.node.node(
        type="groups",
        name="groups",
        definition="groups",
        doxygen_id="groups",
        parent=doxycast.config.project_roots[project],
        children=[],
        brief="Groups Root",
        details=textwrap.dedent("""
            The groups node of the project. This node is a special type of
            node, with all other nodes representing group within the same
            project referenced hierarchically. Documentation for this node
            should never be generated.
        """)
    )

    specials = doxycast.node.node(
        type="specials",
        name="specials",
        definition="specials",
        doxygen_id="specials",
        parent=doxycast.config.project_roots[project],
        children=[],
        brief="Doxygen special nodes",
        details=textwrap.dedent("""
            The parent all Doxygen special node of the project. This node is a
            special type of node, with all other Doxygen specific nodes within
            the same project referenced hierarchically. Documentation for this
            node should never be generated.
        """)
    )

    while len(doxycast.config.project_roots[project].children) != 0:
        node = doxycast.config.project_roots[project].children[0]
        if node.type in ["dir", "file"]:
            node.reparent(root_directory)
        elif node.type == "group":
            node.reparent(groups)
        elif node.type == "page":
            node.reparent(specials)
        else:
            node.reparent(global_namespace)

    doxycast.config.project_roots[project].children.extend([
        global_namespace,
        groups,
        root_directory,
        specials
    ])

    def move_to_global(node: doxycast.node.node):
        if node.type not in ["dir", "file"]:
            node.reparent(global_namespace)

        for child in node.children:
            move_to_global(child)

    move_to_global(root_directory)

    def rm_group_duplicates(node: doxycast.node.node):
        if node.type not in ["group", "groups"]:
            node.parent.children.append(global_namespace.child(node.doxygen_id))
            node.parent.children.remove(node)

        for child in node.children:
            rm_group_duplicates(child)

    rm_group_duplicates(groups)

    def optimize_node(node: doxycast.node.node):
        node.metadata = node.__dict__.get("metadata", dict())

        if node.type == "variable":

            # HEADS UP! Doxygen parses ``typedef const int c`` as ``variable``
            # ``const typedef int c`` due to a bug.
            if "misinterpreted_typedef_0" in doxycast.config.configuration["projects"][project]["fixes"]:
                if node.definition.startswith("const typedef"):
                    node.definition = node.definition.replace("const typedef", "typedef const")
                    node.type = "typedef"

        if node.type == "function":
            node.parameters = node.__dict__.get("parameters", dict())
            node.definition = (
                node.definition
                .replace(" *", "* ")
                .replace(" &", "& ")
                .replace(" >", ">")
                .replace("< ", "<")
                .replace(" ,", ",")
            )
            node.returns = node.metadata.get("return", str()).strip()

            for parameter in node.parameters:
                try:
                    parameter["doc"] = \
                        node.metadata.get("param", dict()).get(parameter["name"], str()).strip()
                except KeyError:
                    pass

        elif node.type == "namespace":
            node.definition = f"namespace {node.name}"

        elif node.type == "class":
            node.definition = f"class {node.name}"

        elif node.type == "struct":
            node.definition = f"struct {node.name}"

        elif node.type == "union":
            node.definition = f"union {node.name}"

        elif node.type == "enum":
            node.definition = f"enum {node.name}{f' : {node.value_type}' if node.value_type else str()}"

        try:
            for parameter in node.template_parameters:
                try:
                    parameter["doc"] = \
                        node.metadata.get("templateparam", dict()).get(parameter["name"], str()).strip()
                except KeyError:
                    pass
        except AttributeError:
            pass

        node.author     = node.metadata.get("author",     str()).strip()
        node.copyright  = node.metadata.get("copyright",  str()).strip()
        node.version    = node.metadata.get("version",    str()).strip()
        node.date       = node.metadata.get("date",       str()).strip()
        node.attributes = node.metadata.get("attributes", dict())

        node.brief = node.brief.strip()
        node.details = node.details.strip()

        try:
            operators = [
                r"<",
                r"<=",
                r">",
                r">=",
                r"==",
                r"!=",
                r"<=>",
                r"=",
                r"&&",
                r"==",
                r"!",
                r"\+",
                r"\+=",
                r"\-",
                r"\-=",
                r"\*",
                r"\*=",
                r"/",
                r"/=",
                r"%",
                r"%=",
                r"\|",
                r"\|=",
                r"&",
                r"&=",
                r"~",
                r"~=",
                r"<<",
                r"<<=",
                r">>",
                r">>=",
                r"\^",
                r"\^=",
                r"->",
                r"->\*",
                r",",
                r"\[\]",
                r"\(\)",
                r'""\s*[0-9a-zA-Z_]*',
                r"(\s+([a-zA-Z_][0-9a-zA-Z_<>]*::)*[a-zA-Z_][0-9a-zA-Z_<>]*)"
            ]
            operators.sort(reverse=True)
            expression = (
                r"(enum\s+|[^\(]+?\s+|^)(([a-zA-Z_][0-9a-zA-Z_<>]*::)*(operator({operators})|~?[a-zA-Z_][0-9a-zA-Z_<>]*))(\(|;|\s+:|$)"
                .format(operators="|".join(operators))
            )
            node.fully_qualified_name = re.match(expression, node.definition).group(2)

            if node.type == "function":
                node.fully_qualified_name += "("

                for parameter in node.parameters:
                    node.fully_qualified_name += re.sub(r":ref:`(.*?)(\s*<.*?>)?`", r"\1", (
                        parameter["type"]
                        .replace(" *", "* ")
                        .replace(" &", "& ")
                        .replace(" >", ">")
                        .replace("< ", "<")
                    )) + ", "

                if len(node.parameters) != 0:
                    node.fully_qualified_name = node.fully_qualified_name[:-2]

                node.fully_qualified_name += ")"
                node.fully_qualified_name = (
                    node.fully_qualified_name
                    .replace(" , ", ", ")
                    .replace(" )", ")")
                )

                if node.const_qualified:
                    node.fully_qualified_name += " const"

        except AttributeError:
            node.fully_qualified_name = None

        try:
            templatedef = "template <"

            for template_parameter in node.template_parameters:
                templatedef += template_parameter["type"]
                if template_parameter.get("default", None) != None:
                    templatedef += " = " + template_parameter["default"]
                templatedef += ", "

            templatedef = templatedef[:-2]
            templatedef += "> "

            templatedef = (
                templatedef
                .replace(" , ", ", ")
                .replace(" )", ")")
            )

            node.definition = templatedef + node.definition
        except AttributeError:
            pass

        del node.metadata

        for child in node.children:
            optimize_node(child)

    optimize_node(doxycast.config.project_roots[project])
