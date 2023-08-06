"""
Original source: https://github.com/dmyersturnbull/tyrannosaurus
Copyright 2020–2021 Douglas Myers-Turnbull
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

Command-line interface.
"""
from __future__ import annotations

import logging
import os
from pathlib import Path
from subprocess import check_call  # nosec
from typing import Optional, Sequence

import typer

from tyrannosaurus.clean import Clean
from tyrannosaurus.conda import CondaEnv, Recipe
from tyrannosaurus.context import Context
from tyrannosaurus.enums import DevStatus, License
from tyrannosaurus.helpers import _Env
from tyrannosaurus.new import New
from tyrannosaurus.sync import Sync
from tyrannosaurus.update import Update

logger = logging.getLogger(__package__)


class _DevNull:  # pragma: no cover
    """Pretends to write but doesn't."""

    def write(self, msg):
        pass

    def flush(self):
        pass

    def close(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


def write_info():
    # avoid importing above, just in case a user runs --version, --info, or info on an improperly installed version
    from tyrannosaurus import __date__, __version__

    typer.echo(f"Tyrannosaurus v{__version__} ({__date__})")


class CliState:  # pragma: no cover
    def __init__(self):
        self.dry_run = False
        self.verbose = False

    def callback(
        self,
        version: bool = False,
        info: bool = False,
        dry_run: bool = False,
        verbose: bool = False,
    ):
        """
        Tyrannosaurus.
        Tyrannosaurus can create new modern Python projects from a template
        and synchronize metadata across the project.

        Args:
            version: Write version and exit
            info: Write info and exit (same as 'tyrannosaurus info')
            dry_run: Just say what would be done; don't write to the filesystem
            verbose: Output more information
        """
        if version or info:
            write_info()
            raise typer.Exit()
        self.dry_run = dry_run
        self.verbose = verbose


state = CliState()
cli = typer.Typer(callback=state.callback, add_completion=True)


class CliCommands:

    _APACHE2 = typer.Option("apache2")
    _ENV_YAML = Path("environment.yml")

    @staticmethod
    @cli.command()
    def new(
        name: str,
        license: License = _APACHE2,
        user: Optional[str] = None,
        authors: Optional[str] = None,
        description: str = "A Python project",
        keywords: str = "",
        version: str = "0.1.0",
        status: Optional[DevStatus] = None,
        track: bool = False,
        tyranno: str = "current",
        newest=typer.Option(False, hidden=True),
        prompt: bool = False,
    ) -> None:  # pragma: no cover
        """
        Creates a new project.
        Args:
            name: The name of the project, including any dashes or capital letters
            license: The name of the license. One of: apache2, cc0, ccby, ccbync, gpl3, lgpl3, mit
            user: Github repository user or org name
            authors: List of author names, comma-separated
            description: A <100 char description for the project
            keywords: A list of <= 5 keywords, comma-separated
            version: A semantic version (for your project)
            status: A PyPi classifier for development status;
                    if None, defaults to "alpha" if version<1.0 else "production"
            track: Track a remote repo (should be an empty repo; otherwise there will be a merge conflict)
            tyranno: Version of tyrannosaurus to use as the template; can be:
                     an exact version number,
                     'current' for the currently installed version,
                     'stable' for the latest stable version,
                     or 'latest' for the bleeding-edge version
            newest: Same as '--tyranno latest' (deprecated)
            prompt: Prompt for info
        """
        if version.startswith("v"):
            version = version[1:]
        if status is None:
            status = DevStatus.guess_from_version(version)
        if prompt:
            name = typer.prompt("name", type=str, default=name)
            description = typer.prompt("description", type=str, default="A new project")
            version = typer.prompt("version", type=str, default="0.1.0")
            if version.startswith("v"):
                version = version[1:]
            if status is None:
                status = DevStatus.guess_from_version(version)
            status = typer.prompt("status", type=DevStatus, default=status)
            license = typer.prompt("license", type=License, default="apache2").lower()
            user = typer.prompt(
                "user", type=str, prompt_suffix=" [default: from 'git config']", default=user
            )
            authors = typer.prompt(
                "authors",
                type=str,
                prompt_suffix=" [comma-separated; default: from 'git config']",
                default=authors,
            )
            description = typer.prompt("description", type=str, default=description)
            keywords = typer.prompt(
                "keywords", type=str, prompt_suffix=" [comma-separated]", default=keywords
            )
            track = typer.prompt("track", type=bool, default=track)
            tyranno = typer.prompt(
                "tyranno",
                type=str,
                prompt_suffix=" ['current', 'stable', 'latest', or a version]",
                default=tyranno,
            )
        e = _Env(user=user, authors=authors)
        keywords = keywords.split(",")
        path = Path(name)
        # for backwards-compat only
        if newest and tyranno == "current":
            tyranno = "latest"
        New(
            name,
            license_name=license,
            username=e.user,
            authors=e.authors,
            description=description,
            keywords=keywords,
            version=version,
            status=status,
            should_track=track,
            tyranno_vr=tyranno,
        ).create(path)
        typer.echo(f"Done! Created a new repository under {name}")
        typer.echo(
            "See https://tyrannosaurus.readthedocs.io/en/latest/guide.html#to-do-list-for-new-projects"
        )

    @staticmethod
    @cli.command()
    def sync() -> None:  # pragma: no cover
        """
        Syncs project metadata between configured files.
        """
        dry_run = state.dry_run
        context = Context(Path(os.getcwd()), dry_run=dry_run)
        typer.echo("Syncing metadata...")
        typer.echo("Currently, only targets 'init' and 'recipe' are implemented.")
        targets = Sync(context).sync()
        typer.echo(f"Done. Synced to {len(targets)} targets: {targets}")

    @staticmethod
    @cli.command()
    def env(
        path: Path = _ENV_YAML,
        name: Optional[str] = None,
        dev: bool = False,
        extras: bool = False,
    ) -> None:  # pragma: no cover
        """
        Generates an Anaconda environment file.

        Args:
            path: Write to his path
            name: The name of the environment; defaults to the project name
            dev: Include development/build dependencies
            extras: Include optional dependencies
        """
        dry_run = state.dry_run
        typer.echo("Writing environment file...")
        context = Context(Path(os.getcwd()), dry_run=dry_run)
        if name is None:
            name = context.project
        CondaEnv(name, dev=dev, extras=extras).create(context, path)
        typer.echo(f"Wrote environment file {path}")

    @staticmethod
    @cli.command()
    def recipe() -> None:  # pragma: no cover
        """
        Generates a Conda recipe using grayskull.
        """
        dry_run = state.dry_run
        context = Context(Path(os.getcwd()), dry_run=dry_run)
        output_path = context.path / "recipes"
        Recipe(context).create(output_path)
        typer.echo(f"Generated a new recipe under {output_path}")

    @staticmethod
    @cli.command()
    def update(dry_run: bool = False) -> None:  # pragma: no cover
        context = Context(Path(os.getcwd()), dry_run=dry_run)
        updates, dev_updates = Update(context).update()
        typer.echo("Main updates:")
        for pkg, (old, up) in updates.items():
            typer.echo(f"    {pkg}:  {old} --> {up}")
        typer.echo("Dev updates:")
        for pkg, (old, up) in dev_updates.items():
            typer.echo(f"    {pkg}:  {old} --> {up}")
        if not state.dry_run:
            logger.error("Auto-fixing is not supported yet!")

    @staticmethod
    @cli.command()
    def clean(
        dists: bool = False, aggressive: bool = False, hard_delete: bool = False
    ) -> None:  # pragma: no cover
        """
        Removes unwanted files.
        Deletes the contents of ``.tyrannosaurus``.
        Then trashes temporary and unwanted files and directories to a tree under ``.tyrannosaurus``.

        Args:
            dists: Remove dists
            aggressive: Delete additional files, including .swp and .ipython_checkpoints.
            hard_delete: If true, call shutil.rmtree instead of moving to .tyrannosaurus
        """
        dry_run = state.dry_run
        trashed = Clean(dists, aggressive, hard_delete, dry_run).clean(Path(os.getcwd()))
        typer.echo(f"Trashed {len(trashed)} paths.")

    @staticmethod
    @cli.command()
    def info() -> None:  # pragma: no cover
        """
        Prints Tyrannosaurus info.
        """
        write_info()

    @staticmethod
    @cli.command()
    def build(bare: bool = False, dry: bool = False) -> None:  # pragma: no cover
        """
        Syncs, builds, and tests your project.

        If ``bare`` is NOT set, runs:
            - tyrannosaurus sync
            - poetry lock
            - tox
            - tyrannosaurus clean

        z----------------------------------------z
        If the ``bare`` IS set:
        Runs the commands without tox and without creating a new virtualenv.
        This can be useful if you're using Conda and have a dependency only available through Anaconda.
        It's also often faster.
        This command is for convenience and isn't very customizable.
        In this case, runs:
            - tyrannosaurus sync
            - poetry lock
            - pre-commit run check-toml
            - pre-commit run check-yaml
            - pre-commit run check-json
            - poetry check
            - poetry build
            - poetry install -v
            - poetry run pytest --cov
            - poetry run flake8 tyrannosaurus
            - poetry run flake8 docs
            - poetry run flake8 --ignore=D100,D101,D102,D103,D104,S101 tests
            - sphinx-build -b html docs docs/html
            - tyrannosaurus clean
            - pip install .
        z----------------------------------------z

        Args:
            bare: Do not use tox or virtualenv. See above.
            dry: Just output the commands to stdout (don't run them). Useful for making a script template.
        """
        CliCommands.build_internal(bare=bare, dry=dry)

    @staticmethod
    def build_internal(bare: bool = False, dry: bool = False) -> Sequence[str]:
        split = CliCommands.build.__doc__.split("-" * 40)
        cmds = [
            line.strip(" -")
            for line in split[1 if bare else 0].splitlines()
            if line.strip().startswith("- ")
        ]
        if not dry:
            for cmd in cmds:
                logger.info("Running: " + cmd)
                check_call(cmd.split(" "))  # nosec
        return cmds


if __name__ == "__main__":
    cli()
