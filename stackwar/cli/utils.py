import sys
from typing import Optional

import click

from stackwar.surveyutils import iter_squashed


def mostly_sanitize(lang: str, year: int) -> Optional[str]:
    from stackwar.languages import unalias, get_ban, is_known

    real = unalias(lang.lower(), year)

    if real is None:
        return None

    ban = get_ban(real)
    if ban:
        click.secho(f"{lang!r} is not supported: {ban}", fg='red')
        sys.exit(1)

    if not is_known(real):
        click.secho(f"Unknown language {lang!r}", fg='red')
        sys.exit(1)

    return real


def sanitize(lang: str, year: int) -> str:
    real = mostly_sanitize(lang, year)

    if real is None:
        click.secho(f"No data for {lang} in {year}", fg='red')
        sys.exit(1)

    return real


@click.command()
@click.option('--year', '-y', type=int, required=True)
def print_languages(year: int) -> None:
    languages = set()

    for used, want in iter_squashed(year):
        languages.update(used)
        languages.update(want)

    print(f"{len(languages)} languages:")

    for lang in sorted(languages):
        print(lang)
