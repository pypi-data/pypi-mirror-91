# Copyright 2019 Genymobile
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
"""
gmsaas entry point
"""

import sys

import click

import gmsaas
from gmsaas.cli.clioutput import ui
from gmsaas.cli.auth import auth
from gmsaas.cli.config import config
from gmsaas.storage.configcache import PROXY_KEY
from gmsaas.cli.recipes import recipes_cmd_group
from gmsaas.cli.instances import instances_cmd_group
from gmsaas.cli.logzip import logzip
from gmsaas.gmsaas.logger import set_verbosity, LOGGER
from gmsaas.gmsaas.proxy import setup_proxy
from gmsaas.cli.clioutput import OutputFormat, OUTPUT_FORMATS


def get_loggable_args(args):
    """
    Return the args list to log, critical data are removed.
    """
    command = []
    command_idx = 0
    for idx, arg in enumerate(args):
        if not arg.startswith("-"):
            command.append(arg)
            command_idx = idx
            if command in (["auth", "login"], ["config", "set", PROXY_KEY]):
                return args[: command_idx + 1]
    return args


def show_verbose(ctx, _, value):
    """ Eager option, enable logging on stdout """
    if not value or ctx.resilient_parsing:
        return
    set_verbosity(value)


def set_output_format(ctx, _, value):
    """ Eager option, set output format """
    if not value or ctx.resilient_parsing:
        return
    OutputFormat.from_option = value


def show_version(ctx, _, value):
    """ Eager option, show version and exit gmsaas

    To provide several `--version` outputs depending on `--format` option
    we use a custom callback with the help of Click Eager option concept, see
    https://click.palletsprojects.com/en/7.x/options/#callbacks-and-eager-options
    To make it working, `--verbose` and `--format` should be Eager options too.
    Limitation:
    Eager options are evaluated by the order the user provides them to the script.
    As `--version` callback exits gmsaas, `gmsaas --version --format json` would
    output text format, but `gmsaas --format json --verbose --version` works fine.
    """
    if not value or ctx.resilient_parsing:
        return
    ui().show_version(gmsaas.get_name(), gmsaas.get_version(), gmsaas.get_doc_url(), gmsaas.get_pypi_url())
    ctx.exit()


@click.group()
@click.option(
    "--verbose",
    "-v",
    count=True,
    is_eager=True,
    callback=show_verbose,
    expose_value=False,
    help="Print logs in stdout.",
)
@click.option(
    "--format",
    type=click.Choice(OUTPUT_FORMATS),
    is_eager=True,
    expose_value=False,
    callback=set_output_format,
    help="Output format to use. You can set a default format with 'gmsaas config set output-format <format>'.",
)
@click.option(
    "--version",
    is_flag=True,
    is_eager=True,
    expose_value=False,
    callback=show_version,
    help="Show the version and exit.",
)
@click.pass_context
def main(ctx):
    """
    Command line utility for Genymotion SaaS
    """
    LOGGER.info("==== START args: %s ====", get_loggable_args(sys.argv[1:]))
    setup_proxy()
    ctx.ensure_object(dict)


main.add_command(auth)
main.add_command(config)
main.add_command(instances_cmd_group)
main.add_command(recipes_cmd_group)
main.add_command(logzip)


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
