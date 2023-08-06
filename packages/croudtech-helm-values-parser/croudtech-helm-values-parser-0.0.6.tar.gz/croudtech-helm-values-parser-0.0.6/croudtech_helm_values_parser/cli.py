import collections
import json
import os
from pathlib import Path

import click
import ruamel.yaml

from .git_values import GitValues
from .values_parser import ValuesParser

yaml = ruamel.yaml.YAML()


# def dict_merge(a, b, path=None):
#     "merges b into a"
#     if path is None:
#         path = []
#     for key in b:
#         if key in a:
#             if isinstance(a[key], dict) and isinstance(b[key], dict):
#                 dict_merge(a[key], b[key], path + [str(key)])
#         else:
#             a[key] = b[key]
#     return a


@click.group()
@click.option("--debug/--no-debug", default=False)
@click.option("--json-indent", default=2)
@click.pass_context
def cli(ctx, debug, json_indent):
    # ensure that ctx.obj exists and is a dict (in case `cli()` is called
    # by means other than the `if` block below)
    ctx.ensure_object(dict)
    ctx.obj["DEBUG"] = debug
    ctx.obj["JSON_INDENT"] = None if json_indent == 0 else json_indent


@cli.command()
@click.pass_context
@click.option("--repo", required=True, help="Path to the values repo")
@click.option("--property-key", required=True, help="Path to the values repo")
@click.option(
    "--environment", multiple=True, required=False, help="Specify environment names"
)
@click.option(
    "--namespace", multiple=True, required=False, help="Specify namespace names"
)
@click.option(
    "--chart", multiple=True, required=False, help="Specify chart names", default=[]
)
@click.option(
    "--output",
    required="true",
    default="json",
    help="The output format",
    type=click.Choice(["json", "text"]),
)
def extrapolate_property(
    ctx, repo, property_key, environment, namespace, chart, output
):
    vp = ValuesParser(
        repo=repo, output_format=output, output_indent=ctx.obj["JSON_INDENT"]
    )
    print(
        vp.get_release_properties(
            key=property_key,
            environments=environment,
            namespaces=namespace,
            charts=chart,
        ),
    )


@cli.command()
@click.pass_context
@click.option("--repo", required=True, help="Path to the values repo")
@click.option("--destination", required=True, help="Path to the destination folder")
@click.option(
    "--environment", multiple=True, required=False, help="Specify environment names"
)
@click.option(
    "--namespace", multiple=True, required=False, help="Specify namespace names"
)
@click.option(
    "--chart", multiple=True, required=False, help="Specify chart names", default=[]
)
@click.option(
    "--output",
    required="true",
    default="yaml",
    help="The output format",
    type=click.Choice(["json", "yaml"]),
)
@click.option(
    "--encryption-password",
    multiple=False,
    required=False,
    help="Provide a password to encrypt the output files",
)
def build_all_values_files(
    ctx, repo, destination, environment, namespace, chart, output, encryption_password
):
    vp = ValuesParser(
        repo=repo, output_format=output, output_indent=ctx.obj["JSON_INDENT"]
    )
    print(
        vp.build_all_values_files(
            destination=destination,
            environments=environment,
            namespaces=namespace,
            charts=chart,
            output_type=output,
            encryption_password=encryption_password,
        ),
    )


@cli.command()
@click.pass_context
@click.option("--repo", required=True, help="Path to the values repo")
@click.option("--destination", required=True, help="Path to the destination folder")
@click.option(
    "--environment", multiple=False, required=False, help="Specify environment name"
)
@click.option(
    "--namespace", multiple=False, required=False, help="Specify namespace name"
)
@click.option(
    "--chart", multiple=False, required=False, help="Specify chart name", default=[]
)
@click.option(
    "--app-name", multiple=False, required=False, help="Specify app name", default=[]
)
@click.option(
    "--output",
    required="true",
    default="yaml",
    help="The output format",
    type=click.Choice(["json", "yaml"]),
)
@click.option(
    "--encryption-password",
    multiple=False,
    required=False,
    help="Provide a password to encrypt the output files",
)
def build_single_values_file(
    ctx,
    repo,
    destination,
    environment,
    namespace,
    chart,
    app_name,
    output,
    encryption_password,
):
    vp = ValuesParser(
        repo=repo, output_format=output, output_indent=ctx.obj["JSON_INDENT"]
    )
    print(
        vp.build_single_values_file(
            destination=destination,
            environments=environment,
            namespaces=namespace,
            charts=chart,
            output_type=output,
            app_name=app_name,
            encryption_password=encryption_password,
        ),
    )


# @cli.command()
# @click.pass_context
# @click.option("--namespace", default="default", help="The namespace for the release")
# @click.option("--chart", default="nginx", help="The name of the chart")
# @click.option("--app", required="true", help="The app name for the release")
# @click.option("--extrafiles", help="Extra file names to search for")
# @click.option("--extravalues", help="Full paths to extra values files")
# @click.option(
#     "--destination", default=os.getcwd() + "/tmp/helm-values", help="The destination for downloaded values files"
# )
# @click.option(
#     "--output",
#     required="true",
#     default="json",
#     help="The source s3 bucket name",
#     type=click.Choice(["json", "helm", "combined"]),
# )
# @click.option("--region", default="eu-west-2", help="The target region")
# @click.option("--envname", default="development", help="The target environment")
# @click.option("--colour", default="blue", help="The target colour")
# def get_values(
#     ctx,
#     namespace,
#     chart,
#     app,
#     extrafiles,
#     extravalues,
#     destination,
#     output,
#     region,
#     envname,
#     colour,
# ):
#     """Build all possible paths for values files"""
#     if extrafiles == None:
#         extrafiles = []
#     else:
#         extrafiles = extrafiles.split(",")
#     if extravalues == None:
#         extravalues = []
#     else:
#         extravalues = extravalues.split(",")

#     bp = GitValues(namespace, chart, app, region, extrafiles, extravalues)
#     bp = GitValues(
#         namespace=namespace,
#         chart=chart,
#         app=app,
#         colour=colour,
#         envname=envname,
#         region=region,
#         extra_files=extrafiles,
#         extra_values=extravalues,
#     )

#     downloaded = bp.download_values(destination)
#     if output == "json":
#         print(json.dumps(downloaded))
#     elif output == "combined":
#         combined = {}
#         for file in downloaded:
#             click.echo("Adding " + file)
#             with open(file) as fp:
#                 data = yaml.load(fp)
#                 combined = dict_merge(dict(data), dict(combined))
#         filename = destination + os.path.sep + "combined-%s-%s.yaml" % (namespace, app)
#         fout = open(filename, "w+")
#         yaml.dump(combined, fout)
#         fout.close()
#         print(filename)
#     elif output == "helm":
#         helm_args = ""
#         for file in downloaded:
#             helm_args = helm_args + " --values " + file
#         print(helm_args)


if __name__ == "__main__":
    cli()
