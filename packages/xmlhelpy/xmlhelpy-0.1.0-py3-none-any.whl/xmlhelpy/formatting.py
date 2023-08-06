# Copyright 2020 Karlsruhe Institute of Technology
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
import click
from lxml import etree


def _try_parsing_args(ctx):
    params = list(ctx.command.params)

    # Try parsing the default arguments to make sure the command exits instead of
    # printing some help text and pretending everything is fine.
    while True:
        try:
            ctx.command.parse_args(ctx, ctx.args)
            break
        except click.exceptions.MissingParameter as e:
            # Ignore required parameters without default values and try again.
            ctx.command.params.remove(e.param)

    ctx.command.params = params


def print_xmlhelp(ctx, param, value, **kwargs):
    """Print the XML help message and exit."""
    if not value:
        return

    _try_parsing_args(ctx)

    program_elem = ctx.command.to_xml()

    # Always list all arguments first.
    sorted_params = sorted(
        ctx.command.params,
        key=lambda param: param.param_type_name,
    )

    for index, _param in enumerate(sorted_params):
        if _param.name not in ["help", "xmlhelp"]:
            program_elem.append(_param.to_xml(index))

    xml = etree.tostring(
        program_elem,
        pretty_print=True,
        xml_declaration=True,
        encoding="UTF-8",
    )

    # Do not print the additional newline.
    click.echo(xml.decode()[:-1])
    ctx.exit()
