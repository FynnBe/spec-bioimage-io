from pprint import pprint

import typer

from bioimageio.spec import __version__, commands

help_version = f"bioimageio.spec package version {__version__}"
app = typer.Typer(
    help=help_version,
    context_settings={"help_option_names": ["-h", "--help", "--version"]},  # make --version display help with version
)  # https://typer.tiangolo.com/


@app.command()
def validate(
    rdf_source: str = typer.Argument(..., help="RDF source as relative file path or URI"),
    update_format: bool = typer.Option(
        False,
        help="Update format version to the latest (might fail even if source adheres to an old format version). "
        "To inform the format update the source may specify fields of future versions in "
        "config:future:<future version>.",  # todo: add future documentation
    ),
    update_format_inner: bool = typer.Option(
        None, help="For collection RDFs only. Defaults to value of 'update-format'."
    ),
    verbose: bool = typer.Option(False, help="show traceback of unexpected (no ValidationError) exceptions"),
) -> int:
    summary = commands.validate(rdf_source, update_format, update_format_inner)
    if summary["error"] is not None:
        print(f"Error in {summary['name']}:")
        pprint(summary["error"])
        if verbose:
            print("traceback:")
            pprint(summary["traceback"])
        return 1
    else:
        print(f"No validation errors for {summary['name']}")
        return 0


validate.__doc__ = commands.validate.__doc__

# single command requires additional dummy callback
# see: https://typer.tiangolo.com/tutorial/commands/one-or-multiple/#one-command-and-one-callback
@app.callback()
def callback():
    typer.echo(help_version)  # use this callback to print out version


if __name__ == "__main__":
    app()
