import typer as tp

from PACKAGE_NAME.cli import sample

app = tp.Typer(
    name="PACKAGE_NAME",
    pretty_exceptions_enable=False,
    no_args_is_help=True,
)

# Add the subcommands to the main typer application
app.add_typer(sample.group, name="samples")
