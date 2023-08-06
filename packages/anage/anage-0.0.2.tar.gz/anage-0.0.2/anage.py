# Python package manager
# Copyright (C) 2021  Nguyễn Gia Phong
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from collections import defaultdict, deque
from os.path import basename
from pathlib import Path
from subprocess import run
from sys import executable
from textwrap import indent, wrap

from appdirs import user_data_dir
from click import argument, group
from packaging.requirements import Requirement

try:
    from importlib.metadata import distributions
except ModuleNotFoundError:
    from importlib_metadata import distributions

__doc__ = 'python -manage packages'
__version__ = '0.0.2'


def ensure_manual():
    """Ensure the file storing manually installed packages exists.

    Return the path to it.
    """
    directory = Path(user_data_dir('anage'))
    file = directory / 'manual'
    if not file.exists():
        # Minimal environment plus anage itself
        file.write_text('anage\npip\npkg-resources\nsetuptools\n')
    return file


def dependency_graph():
    """Return the current dependency graph."""
    vertices, edges = set(), defaultdict(set)
    for distribution in distributions():
        d = distribution.metadata['Name']
        vertices.add(d)
        for r in distribution.requires or []:
            requirement = Requirement(r)
            marker = requirement.marker
            if marker is None or marker.evaluate({'extra': ''}):
                edges[d].add(requirement.name)
    return vertices, edges


def dependencies(edges, packages):
    """Return implicit dependencies of given packages."""
    result, queue = set(), deque(packages)
    while queue:
        v = queue.popleft()
        if v in result: continue
        result.add(v)
        queue.extend(edges[v])
    return result


def dependents(edges, packages):
    """Return implicit dependents of given packages."""
    egdes = defaultdict(set)
    for k, v in edges.items():
        for i in v: egdes[i].add(k)
    return dependencies(egdes, packages)


@group(context_settings={'help_option_names': ('-h', '--help')})
def cli():
    """Manage Python packages."""


@cli.command()
@argument('requirements', nargs=-1)
def install(requirements):
    """Install distributions specified as requirements."""
    reqset = set(requirements)
    run((executable, '-m', 'pip', 'install', *reqset))

    file = ensure_manual()
    manual = reqset.union(file.read_text().strip().split())
    file.write_text(''.join(f'{r}\n' for r in sorted(manual)))
    print('Marked the following packages as manually installed:')
    print(indent('\n'.join(wrap(' '.join(sorted(reqset)))), '  '))


@cli.command()
@argument('distributions', nargs=-1)
def remove(distributions):
    """Remove distributions and automatically installed dependencies."""
    file = ensure_manual()
    vertices, edges = dependency_graph()

    must_remove = dependents(edges, distributions)
    manual = set(file.read_text().strip().split())
    must_keep = manual.difference(must_remove)
    should_keep = dependencies(edges, must_keep)
    should_remove = vertices.difference(should_keep)

    print('Remove the following packages?  (^C to abort)')
    input(indent('\n'.join(wrap(' '.join(sorted(should_remove)))), '  '))
    run((executable, '-m', 'pip', 'uninstall', '-y', *should_remove))
    file.write_text(''.join(f'{r}\n' for r in sorted(
        manual.intersection(should_keep))))


if __name__ == '__main__':
    cli(prog_name=f'{basename(executable)} -manage')
