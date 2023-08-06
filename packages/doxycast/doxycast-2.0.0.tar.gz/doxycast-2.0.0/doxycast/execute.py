import doxycast.config
import doxycast.utils
from doxycast.utils import ansi_colors

import io
import os
import sys
import subprocess
import tempfile
import textwrap
import shutil
import sphinx.errors

template_doxygen_config = textwrap.dedent("""
    CREATE_SUBDIRS           =      NO

    RECURSIVE                =      YES

    FULL_PATH_NAMES          =      YES

    OUTPUT_DIRECTORY         =      {output_dir}

    GENERATE_HTML            =      NO
    GENERATE_LATEX           =      NO
    GENERATE_XML             =      YES

    XML_PROGRAMLISTING       =      YES

    ALIASES                  =      rst="@verbatim embed:rst:leading-asterisk"
    ALIASES                 +=      endrst="@endverbatim"

    ALIASES                 +=      attr="@verbatim attributes:leading-asterisk"
    ALIASES                 +=      endattr="@endverbatim"

    ENABLE_PREPROCESSING     =      YES
    MACRO_EXPANSION          =      YES
    EXPAND_ONLY_PREDEF       =      NO
    SKIP_FUNCTION_MACROS     =      NO

    PREDEFINED               =      DOXYGEN_DOCUMENTATION_BUILD
    PREDEFINED              +=      DOXYGEN_SHOULD_SKIP_THIS

    {user_defined_config}
""")

def execute_doxygen(project: str):
    """
    Executes Doxygen.
    """
    config = doxycast.config.configuration["projects"][project]

    if not config["execute_doxygen"]:
        return

    print(
        (' ' * shutil.get_terminal_size().columns) + "\r", # Clean the line
        doxycast.utils.color(ansi_colors.bold) + "doxycast: executing doxygen: ",
        doxycast.utils.color(ansi_colors.magenta) + project,
        doxycast.utils.color(ansi_colors.default),
        sep="",
        end="\n\n" if config["doxygen_verbose"] or config["doxygen_warning"] else "\r"
    )

    doxygen_cmd = [
        "doxygen",
        "-" if config.get("doxygen_config", None) != None else config["doxygen_config_file"]
    ]

    doxygen_streams = {
        "stdout": sys.stdout if config["doxygen_verbose"] else subprocess.DEVNULL,
        "stderr":
            tempfile.TemporaryFile(mode="r+", encoding="utf-8")
                if config["doxygen_warnings_prettify"] else subprocess.STDOUT
                    if config["doxygen_warning"] else subprocess.DEVNULL,
        "stdin": subprocess.PIPE if config.get("doxygen_config", None) else None
    }

    doxygen_proc = subprocess.Popen(doxygen_cmd, **doxygen_streams)
    doxygen_proc.communicate(
        input = bytes(template_doxygen_config.format(
            output_dir=config["xml_dir"],
            user_defined_config=config["doxygen_config"]
        ), "utf-8") if config.get("doxygen_config", None) != None else None
    )

    if config["doxygen_warnings_prettify"]:
        doxygen_streams["stderr"].seek(0)
        warnings: str = doxygen_streams["stderr"].read()
        if not (warnings.isspace() or warnings == str()):
            print()

        sys.stderr.write(
            doxycast.utils.color(ansi_colors.yellow) +
            warnings +
            doxycast.utils.color(ansi_colors.default)
        )

    if doxygen_proc.returncode != 0:
        raise sphinx.errors.ExtensionError(
            f"Doxygen exited with non-zero status ({doxygen_proc.returncode})"
        )
