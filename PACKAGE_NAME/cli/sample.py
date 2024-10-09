import typing as t

import typer as tp

group = tp.Typer(
    name="samples",
    no_args_is_help=True,
    add_completion=False,
)


@group.command(short_help="This is a hello world example.")
def hello_world(
    name: t.Optional[str] = tp.Option(None, help="Your Name"),
):
    """
    This is a hello world example.
    """
    from rich import print

    msg = f"Hello [bold orange]{name if name is not None else 'World'}[/bold orange] :whale2:!"
    print(msg)
