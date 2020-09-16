import click

from stackwar.surveyutils import iter_squashed


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
