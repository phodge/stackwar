import csv
from typing import Iterator, Set, Tuple

from stackwar import get_squash_path


def get_cols(year: int) -> Tuple[str, str]:
    if year == 2020:
        # Which programming, scripting, and markup languages have you done
        # extensive development work in over the past year, and which do
        # you want to work in over the next year? (If you both worked with
        # the language and want to continue to do so, please check both
        # boxes in that row.)
        usedcol = 'LanguageWorkedWith'
        wantcol = 'LanguageDesireNextYear'
    elif year == 2019:
        # Which of the following programming, scripting, and markup
        # languages have you done extensive development work in over the
        # past year, and which do you want to work in over the next year?
        # (If you both worked with the language and want to continue to do
        # so, please check both boxes in that row.)
        usedcol = 'LanguageWorkedWith'
        wantcol = 'LanguageDesireNextYear'
    elif year == 2018:
        # Which of the following programming, scripting, and markup
        # languages have you done extensive development work in over the
        # past year, and which do you want to work in over the next year?
        # (If you both worked with the language and want to continue to do
        # so, please check both boxes in that row.)
        usedcol = 'LanguageWorkedWith'
        wantcol = 'LanguageDesireNextYear'
    elif year == 2017:
        # Which of the following languages have you done extensive
        # development work in over the past year, and which do you want to
        # work in over the next year?
        usedcol = 'HaveWorkedLanguage'
        wantcol = 'WantWorkLanguage'
    elif year == 2016:
        # Which of the following languages or technologies have you done
        # extensive development with in the last year? (select all that apply)
        usedcol = 'tech_do'
        # Which of the following languages or technologies do you WANT to work
        # with this year? (select all that apply)
        wantcol = 'tech_want'
    else:
        raise Exception(f"Invalid year {year}")

    return usedcol, wantcol


def iter_squashed(year: int) -> Iterator[Tuple[Set[str], Set[str]]]:
    """
    Iterate over squashed data from `year`.

    Yield tuple of 2 items:
    - `used` languages
    - `wanted` languages
    """
    csvpath = get_squash_path(year)

    with csvpath.open() as f:
        reader = csv.reader(f)
        for row in reader:
            used, want = row
            yield set(used.split(":")), set(want.split(":"))
