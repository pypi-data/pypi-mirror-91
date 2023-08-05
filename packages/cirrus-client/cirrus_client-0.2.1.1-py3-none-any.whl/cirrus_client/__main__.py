from os import environ
import time
from contextlib import contextmanager
import sys

import click

import requests

from rich.console import Console
from rich.table import Table

from .about import __version__


console = Console()

bluescreen_message = """[red]FAILURE:[/red] [blue]If nothing happened, something sure happened...[/blue]
Contact to your Cirrus Administrator."""


def duration_pp(sec: float):
    if sec > 60:
        return f"{int(sec / 60)} min {int(sec) % 60} sec"

    return f"{int(sec)} sec"


@contextmanager
def timeit(desc: str):
    t0 = time.time()

    yield

    t1 = time.time()

    console.print(f"{desc} took [bold orange]{duration_pp(t1 - t0)}[/bold orange]")


def route(ctx: dict, handler: str):
    return f"http://{ctx.obj['API_HOST']}:{ctx.obj['API_PORT']}/{handler}"


@click.group()
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, debug):
    ctx.ensure_object(dict)

    ctx.obj['DEBUG'] = debug


@cli.group()
def project():
    """Manage cirrus projects."""
    pass  # pylint: disable=W0107


@cli.command()
def version():
    console.print(f"Cirrus Client [blue]v{__version__}[/blue]")


@cli.command()
@click.pass_context
@click.option('--hostname', '-h', required=True, help="Cirrus API hostname/IP",
              default=environ.get('CIRRUS_HOSTNAME', '127.0.0.1'), show_default=True)
@click.option('--port', '-p', required=True, help="Cirrus API port", default=environ.get('CIRRUS_PORT', 8000),
              show_default=True)
def droplet_types(ctx, hostname, port):
    """List available droplet type options."""
    try:
        d = requests.get(f"http://{hostname}:{port}/droplets")

        if d.status_code != 200:
            console.print(f"Error {d.json()}")
        else:
            d = d.json()

        table = Table(show_header=True, header_style="bold magenta")

        table.add_column("Name", style="dim", width=12)
        table.add_column("Type")
        table.add_column("OS", justify="center")
        table.add_column("Core", justify="right")
        table.add_column("Resource Allocation (cpu)", justify="right")
        table.add_column("Memory", justify="right")
        table.add_column("User Storage", justify="right")
        table.add_column("GA", justify="right")

        for elem in d:
            table.add_row(elem['name'], elem['type'], "CentOS 7.7 x64", str(elem['core']), "Shared",
                          f"{elem['memory']} GB",
                          f"{elem['storage']} GB",
                          ":thumbs_up:" if elem['ga'] else ":thumbs_down:")

        console.print(table)
    except Exception:
        console.log(bluescreen_message)
        if ctx.obj['DEBUG']:
            console.print_exception(show_locals=False)
        sys.exit(1)


@project.command()
@click.pass_context
@click.option('--user', '-u', required=True, help="Cirrus user", default=environ.get('CIRRUS_USER', None),
              show_default=True)
@click.option('--name', '-n', required=True, help="Project name", default=environ.get('CIRRUS_PROJECT', None),
              show_default=True)
@click.option('--hostname', '-h', required=True, help="Cirrus API hostname/IP",
              default=environ.get('CIRRUS_HOSTNAME', '127.0.0.1'), show_default=True)
@click.option('--port', '-p', required=True, help="Cirrus API port", default=environ.get('CIRRUS_PORT', 8000),
              show_default=True)
@click.option("--public-key", "-k", default=None, help="ssh public key.", type=click.File())
def create(ctx, user, name, hostname, port, public_key):
    """Create an empty project."""

    try:
        if public_key is not None:
            public_key_content = public_key.read()
            d = requests.post(f"http://{hostname}:{port}/sync/user/{user}/project/{name}",
                              json=dict(public_key=public_key_content))
        else:
            d = requests.post(f"http://{hostname}:{port}/sync/user/{user}/project/{name}")

        if d.status_code != 200:
            console.print(f"[bold red]FAILED[/bold red]: Project {name} with status code {d.status_code}")
        else:
            console.print(f"[bold green]DONE[/bold green]: Project {name}")
    except:
        console.log(bluescreen_message)
        if ctx.obj['DEBUG']:
            console.print_exception(show_locals=False)
        sys.exit(1)


@project.command()
@click.pass_context
@click.option('--user', '-u', required=True, help="Cirrus user", default=environ.get('CIRRUS_USER', None),
              show_default=True)
@click.option('--name', '-n', required=True, help="Project name", default=environ.get('CIRRUS_PROJECT', None),
              show_default=True)
@click.option('--hostname', '-h', required=True, help="Cirrus API hostname/IP",
              default=environ.get('CIRRUS_HOSTNAME', '127.0.0.1'), show_default=True)
@click.option('--port', '-p', required=True, help="Cirrus API port", default=environ.get('CIRRUS_PORT', 8000),
              show_default=True)
def drop(ctx, user, name, hostname, port):
    """Drop a project and its all resources.
        Use with CAUTION !!!
    """
    try:
        console.print(f"You are about to [bold red]destroy[/bold red] project [bold blue]{name}[/bold blue]")
        if click.confirm("Do you want to continue?"):
            d = requests.delete(f"http://{hostname}:{port}/sync/user/{user}/project/{name}", params=dict(confirm=True))

            if d.status_code != 200:
                console.print(f"[bold red]FAILED[/bold red]: Project {name} with status code {d.status_code}")
            else:
                console.print(f"[bold green]REMOVED[/bold green]: Project {name}")
    except:
        console.log(bluescreen_message)
        if ctx.obj['DEBUG']:
            console.print_exception(show_locals=False)
        sys.exit(1)


@project.command()
@click.pass_context
@click.option('--user', '-u', required=True, help="Cirrus user", default=environ.get('CIRRUS_USER', None),
              show_default=True)
@click.option('--hostname', '-h', required=True, help="Cirrus API hostname/IP",
              default=environ.get('CIRRUS_HOSTNAME', '127.0.0.1'), show_default=True)
@click.option('--port', '-p', required=True, help="Cirrus API port", default=environ.get('CIRRUS_PORT', 8000),
              show_default=True)
def show(ctx, user, hostname, port):
    """Show all of projects"""

    try:
        d = requests.get(f"http://{hostname}:{port}/user/{user}/project").json()

        table = Table(show_header=True, header_style="bold magenta")

        table.add_column("Name")
        table.add_column("Created")
        table.add_column("Last Updated")

        for elem in d:
            table.add_row(elem['name'], elem['created'], elem['modified'])

        console.print(table)
    except:
        console.log(bluescreen_message)
        if ctx.obj['DEBUG']:
            console.print_exception(show_locals=False)
        sys.exit(1)


@project.command()
@click.pass_context
@click.option('--user', '-u', required=True, help="Cirrus user", default=environ.get('CIRRUS_USER', None),
              show_default=True)
@click.option('--name', '-n', required=True, help="Project name", default=environ.get('CIRRUS_PROJECT', None),
              show_default=True)
@click.option('--hostname', '-h', required=True, help="Cirrus API hostname/IP",
              default=environ.get('CIRRUS_HOSTNAME', '127.0.0.1'), show_default=True)
@click.option('--port', '-p', required=True, help="Cirrus API port", default=environ.get('CIRRUS_PORT', 8000),
              show_default=True)
def droplets(ctx, user, name, hostname, port):
    """Show all project droplets"""

    try:
        d = requests.get(f"http://{hostname}:{port}/user/{user}/project/{name}/droplets")

        output = d.json()

        table = Table(show_header=True, header_style="bold magenta")

        table.add_column("Project")
        table.add_column("Type", style="dim", width=12)
        table.add_column("Hostname")
        table.add_column("Public IP")
        table.add_column("Private IP")

        for dtype in set(k.rsplit('-', 1)[0] for k in output):
            for host, ip in zip(output[f"{dtype}-hostname"]['value'], output[f"{dtype}-ip"]['value']):
                table.add_row(name, dtype, host, ip, "")

        console.print(table)
    except:
        console.log(bluescreen_message)
        sys.exit(1)


@project.command()
@click.pass_context
@click.option('--user', '-u', required=True, help="Cirrus user", default=environ.get('CIRRUS_USER', None),
              show_default=True)
@click.option('--name', '-n', required=True, help="Project name", default=environ.get('CIRRUS_PROJECT', None),
              show_default=True)
@click.option('--hostname', '-h', required=True, help="Cirrus API hostname/IP",
              default=environ.get('CIRRUS_HOSTNAME', '127.0.0.1'), show_default=True)
@click.option('--port', '-p', required=True, help="Cirrus API port", default=environ.get('CIRRUS_PORT', 8000),
              show_default=True)
@click.option("--droplet-type", "-t", default="basic-2-4gb", show_default=True)
@click.option("--count", "-c", default=1, show_default=True)
@click.option("--prefix", default=None, help="Not setting will cause random host name.")
@click.option("--data-disk-count", default=0, show_default=True, help="Number of extra data disks.")
@click.option("--data-disk-gb", default=25, show_default=True, help="Disk size in GB.")
@click.option("--data-disk-type", default='xfs', type=click.Choice(['raw', 'ext4', 'xfs']), show_default=True,
              help="File system type.")
def scale(ctx, user, name, hostname, port, droplet_type, count, prefix, data_disk_count, data_disk_gb, data_disk_type):
    """Add/Remove resources into your project."""

    try:
        with timeit(f"Scale project [bold blue]{name}[/bold blue]"):

            d = requests.put(f"http://{hostname}:{port}/sync/user/{user}/project/{name}/scale",
                             json=dict(type=droplet_type, count=count, prefix=prefix, data_disk_size=data_disk_gb,
                                       data_disk_count=data_disk_count,
                                       data_disk_type=data_disk_type))

            if d.status_code != 200:
                console.print(f"[bold red]ERROR[/bold red]: Project {name}")
                console.print(d.json().get('detail', f"Unknown error with code {d.status_code}"))
            else:
                console.print(f"[bold green]SCALED UP/DOWN[/bold green]: Project {name}")
                output = d.json()

                table = Table(show_header=True, header_style="bold magenta")

                table.add_column("Project")
                table.add_column("Type", style="dim", width=12)
                table.add_column("Hostname")
                table.add_column("Public IP")
                table.add_column("Private IP")

                for dtype in set(k.rsplit('-', 1)[0] for k in output):
                    for host, ip in zip(output[f"{dtype}-hostname"]['value'], output[f"{dtype}-ip"]['value']):
                        table.add_row(name, dtype, host, ip, "")

                console.print(table)

            # TODO: Implement this asynchronously
            # TODO: Check login with paramiko

            # NOTE: Use terraform plan to decide whether to continue sync of async
    except:
        console.log(bluescreen_message)
        if ctx.obj['DEBUG']:
            console.print_exception(show_locals=False)
        sys.exit(1)


if __name__ == '__main__':
    cli()
