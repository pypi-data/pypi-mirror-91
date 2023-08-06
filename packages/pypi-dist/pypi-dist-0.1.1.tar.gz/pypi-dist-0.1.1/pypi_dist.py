#!/usr/bin/env python

import os
from pathlib import Path
import shutil
import subprocess

import semver
import click
from git import Repo
from setuptools.sandbox import run_setup

REPO_PATH = Path('.')
VERSION_PATH = Path('.VERSION')
SETUP_PATH = Path('setup.py')
DIST_PATH = Path('dist')
PYPIRC_PATH = Path.home().joinpath('.pypirc')

RELEASE_TYPE_CHOICES = click.Choice(['major', 'minor', 'patch'])


def get_previous_version() -> semver.VersionInfo:
    if VERSION_PATH.exists():
        with open(VERSION_PATH) as version_file:
            return semver.VersionInfo.parse(version_file.read())
    else:
        return None


def get_next_version(previous_version: semver.VersionInfo, release_type: str) -> semver.VersionInfo:
    if previous_version:
        if not release_type:
            # Prompt the user if it was not added as a CLI argument.
            release_type = click.prompt('Release type', type=RELEASE_TYPE_CHOICES)

        release_type = release_type.upper()

        if release_type == 'MAJOR':
            return previous_version.bump_major()
        elif release_type == 'MINOR':
            return previous_version.bump_minor()
        else:
            return previous_version.bump_patch()
    else:
        return semver.VersionInfo.parse('0.1.0')


def validate_version(ctx, param, value) -> semver.VersionInfo:
    if not value:
        return None

    try:
        return semver.VersionInfo.parse(value)
    except ValueError:
        raise click.BadParameter('version must use a valid semver format')


def update_version_file(next_version: semver.VersionInfo):
    with open(VERSION_PATH, 'w') as version_file:
        version_file.write(str(next_version))


def check_for_local_changes(repo: Repo) -> bool:
    return repo.is_dirty(untracked_files=True)


def commit_version_bump(repo: Repo, next_version: semver.VersionInfo):
    repo.index.add([str(VERSION_PATH)])
    repo.index.commit(f'Bumping version to {next_version}')


def is_version_released(repo: Repo, next_version: semver.VersionInfo) -> bool:
    return str(next_version) in repo.tags


def tag_version(repo: Repo, next_version: semver.VersionInfo):
    repo.create_tag(str(next_version))


def push_tag(repo: Repo, next_version: semver.VersionInfo):
    repo.remotes.origin.push(str(next_version))


def pypirc_available() -> bool:
    return PYPIRC_PATH.exists()


@click.command()
@click.option('--release-type', type=RELEASE_TYPE_CHOICES, help='The increment type of this version')
@click.option('--version', callback=validate_version, help='A specific version number to release')
@click.option('--pypi-username', default=lambda: os.environ.get('PYPIDIST_USERNAME'), help='The username for the pypi account to upload to')
@click.option('--pypi-password', default=lambda: os.environ.get('PYPIDIST_PASSWORD'), help='The password for the pypi account to upload to')
def dist_release(release_type, version, pypi_username, pypi_password):
    
    if not (pypi_username and pypi_password):
        if not pypirc_available():
            raise click.ClickException('Pypi username/password must be provided with --pypi-username/--pypi-password arguments, '
                                       'PYPIDIST_USERNAME/PYPIDIST_PASSWORD environment variables, or with a .pypirc file in your home directory.')

    repo = Repo(REPO_PATH)
    local_changes = check_for_local_changes(repo)

    if local_changes:
        raise click.ClickException('The repository has uncommitted changes. Please commit all changes before releasing.')

    try:
        previous_version = get_previous_version()
    except ValueError:
        raise click.ClickException('The version in .VERSION is not a valid semver string. Please check this value.')

    if not version:
        next_version = get_next_version(previous_version, release_type)
    else:
        next_version = version

    if previous_version:
        click.confirm(f'The previous version was {previous_version}. Update to {next_version}?', abort=True)
    else:
        click.confirm(f'This is the first release. Releasing version {next_version}. Continue?', abort=True)

    if is_version_released(repo, next_version):
        raise click.ClickException(f'Version {next_version} has already been released. Please check the value in .VERSION, or specify a version using --version')

    click.echo('Updating .VERSION')
    update_version_file(next_version)

    click.echo(f'Committing version bump to {next_version}')
    commit_version_bump(repo, next_version)

    click.echo(f'Tagging version {next_version}')
    tag_version(repo, next_version)

    click.echo(f'Pushing tag {next_version} to Github')
    push_tag(repo, next_version)

    if DIST_PATH.exists():
        click.echo('Cleaning up dist directory')
        shutil.rmtree(DIST_PATH)

    click.echo('Building source distribution')
    run_setup(str(SETUP_PATH), ['sdist', 'bdist_wheel'])

    click.echo('Publishing artifacts to PyPi')

    if pypi_username and pypi_password:
        subprocess.check_call(['twine', '-u', pypi_username, '-p', pypi_password, 'upload', 'dist/*'])
    else:
        subprocess.check_call(['twine', 'upload', 'dist/*'])
    

if __name__ == '__main__':
    dist_release()
