# zcbe.py - The Z Cross Build Environment
#
# Copyright 2019-2020 Zhang Maiyun
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""The Z Cross Build Environment.

Concepts:
    a build contains many projects
    a projects is just a program/package
"""

import argparse
import asyncio
import os
import sys
import textwrap

from .build import Build
from .exceptions import eprint
from .warner import ZCBEWarner

# All available types of warnings (gcc-like)
ALL_WARNINGS = {
    "name-mismatch": "The project's name specified in conf.toml "
                     "mismatches with that in mapping.toml",
    "lock-exists": "The lock file for a file exists (see zcbe -H lockfile)",
    "generic": "Warnings about ZCBE itself",
    "error": "Error all warnings",
    "all": "Show all warnings",
}

# Gather help strings for all warnings
WARNINGS_HELP = '\n'.join(
    ["{}: {}".format(x, ALL_WARNINGS[x]) for x in ALL_WARNINGS])

DEFAULT_WARNINGS = set((
    "name-mismatch",
    "generic",
)) & set(ALL_WARNINGS)

# Help topics and their help message
TOPICS = {
    "topics": "topics: This list of topics\n"
              "warnings: All available warnings\n"
              "lockfile: Help about lock files\n",
    "warnings": WARNINGS_HELP,
    "lockfile": textwrap.fill("ZCBE builds multiple projects concurrently,"
                              " so a lock file is created to avoid building"
                              " the same project at the same time. Therefore,"
                              " you usually don't have to worry about getting"
                              " -Wlock-exists. However, if this warning"
                              " persists, or you believe something wrong has"
                              " happened, you might want to kill the process,"
                              " remove the lock file, and check if everything"
                              " is OK."),
}


class AboutAction(argparse.Action):
    # pylint: disable=too-few-public-methods
    """Argparse action to show help topics. Exits when finished."""

    def __init__(self, option_strings, dest, nargs=1, **kwargs):
        super().__init__(option_strings, dest, nargs, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        name = values[0]
        try:
            eprint(TOPICS[name], title="")
        except KeyError:
            eprint(f'No such topic "{name}", try "topics" for available ones')
        sys.exit(0)


def start():
    """ZCBE entrypoint. Parse arguments."""
    # Set up the warner to use
    warner = ZCBEWarner()
    warner.load_default(set(ALL_WARNINGS), DEFAULT_WARNINGS)

    # This has to be a internal class as it uses warner
    class WarningsAction(argparse.Action):
        # pylint: disable=too-few-public-methods
        """Argparse action to modify warning behavior."""

        def __init__(self, option_strings, dest, nargs=1, **kwargs):
            super().__init__(option_strings, dest, nargs, **kwargs)

        def __call__(self, parser, namespace, values, option_string=None):
            # First deal with -w
            if option_string[1] == 'w':
                warner.silence()
                return
            # Then deal with -W*
            reverse = False
            name = values[0]
            if name[0:3] == "no-":
                reverse = True
                name = name[3:]
            if name not in ALL_WARNINGS:
                warner.warn("generic", f'No such warning "{name}"')
                return
            if reverse:
                warner.setopts({name: False})
            else:
                warner.setopts({name: True})
    parser = argparse.ArgumentParser(
        description="The Z Cross Build Environment")
    parser.add_argument("-w", help="Suppress all warnings",
                        action=WarningsAction, nargs=0)
    parser.add_argument("-W", metavar="WARNING",
                        help="Modify warning behavior", action=WarningsAction)
    parser.add_argument("-B", "--rebuild", "--always-make", "--always-build",
                        action="store_true",
                        help="Force build requested projects and dependencies")
    parser.add_argument("-C", "--chdir", "--directory", type=str,
                        help="Change directory to")
    parser.add_argument("-o", "--stdout-to", metavar="FILE", type=str,
                        help="Redirect stdout to FILE"
                        " ('{n}' expands to the name of the project)")
    parser.add_argument("-e", "--stderr-to", metavar="FILE", type=str,
                        help="Redirect stderr to FILE"
                        " ('{n}' expands to the name of the project)")
    parser.add_argument("-f", "--file", "--build-toml", type=str,
                        default="build.toml", help="Read FILE as build.toml")
    parser.add_argument("-p", "--prefix", "--override-prefix", type=str,
                        help="Override value for prefix")
    parser.add_argument("-t", "--target-triplet", "--override-target",
                        type=str, help="Override value for target triplet")
    parser.add_argument("-m", "--build-name", "--override-build-name",
                        type=str, help="Override value for build name")
    parser.add_argument("-j", "--jobs", type=int,
                        help="Number of maximum concurrent jobs")
    parser.add_argument("-a", "--all", action="store_true",
                        help="Build all projects in mapping.toml")
    parser.add_argument("-s", "--silent", action="store_true",
                        help="Silence make standard output"
                        "(short for -o /dev/null)")
    parser.add_argument("-n", "--dry-run", "--just-print", "--recon",
                        action="store_true",
                        help="Don't actually run any commands")
    parser.add_argument("-u", "--show-unbuilt", action="store_true",
                        help="List unbuilt projects and exit")
    parser.add_argument("-y", "--yes", action="store_true",
                        help="Assume yes for all questions")
    parser.add_argument("-H", "--about", type=str, action=AboutAction,
                        help='Help on a topic("topics" for a list of topics)')
    parser.add_argument('projects', metavar='PROJ', nargs='*',
                        help='List of projects to build')
    namespace = parser.parse_args()
    return asyncio.run(invoke_builder(namespace, warner))


async def invoke_builder(namespace, warner):
    """Invoke a builder with the arguments."""
    if namespace.chdir:
        os.chdir(namespace.chdir)
    if namespace.silent:
        namespace.stdout_to = os.devnull
    # Create builder instance
    builder = Build(".", warner, if_rebuild=namespace.rebuild,
                    if_dryrun=namespace.dry_run,
                    build_toml_filename=namespace.file,
                    stdout=namespace.stdout_to,
                    stderr=namespace.stderr_to,
                    max_jobs=namespace.jobs or 0,
                    assume_yes=namespace.yes,
                    override_build_name=namespace.build_name,
                    override_prefix=namespace.prefix,
                    override_triplet=namespace.target_triplet)
    if namespace.show_unbuilt:
        return 0 if builder.show_unbuilt() else 1
    if namespace.all:
        result = await builder.build_all()
    else:
        result = await builder.build_many(namespace.projects)
    return result
