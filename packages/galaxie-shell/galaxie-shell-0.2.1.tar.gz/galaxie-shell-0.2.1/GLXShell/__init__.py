from GLXShell.plugins.builtins import PLUGIN_NAME as BUILTINS_NAME
from GLXShell.plugins.builtins import PLUGIN_VERSION as BUILTINS_VERSION
from GLXShell.plugins.builtins import GLXShPluginBuiltins

APPLICATION_AUTHORS = ["Tuuuux"]
APPLICATION_DESCRIPTION = ""
APPLICATION_LICENSE = "GNU General Public License v3 or later (GPLv3+)"
APPLICATION_NAME = "glxsh"
APPLICATION_VERSION = "0.2.1"
APPLICATION_WARRANTY = """Copyright (C) 2020-2021 Galaxie Shell Project.
License GPLv3+: GNU GPL version 3 or later <https://gnu.org/licenses/gpl.html>.
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
"""
APPLICATION_PLUGINS = [
    {
        "name": BUILTINS_NAME,
        "version": BUILTINS_VERSION,
        "object": GLXShPluginBuiltins(),
    },
]
