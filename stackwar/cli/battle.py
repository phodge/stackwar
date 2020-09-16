import csv
from collections import defaultdict
from pathlib import Path
from typing import Dict, Optional, Tuple

import click

from stackwar import DOWNLOAD_LINKS, get_survey_path
from stackwar.cli.utils import mostly_sanitize, sanitize
from stackwar.surveyutils import get_cols, iter_squashed


@click.command()
@click.option('--year', '-y', type=int, required=True)
@click.option('--alt/--no-alt', is_flag=True, default=False)
@click.argument('lang1', required=True)
@click.argument('lang2', required=True)
def battle_text(year: int, lang1: str, lang2: str, alt: bool) -> None:
    usedcol, wantcol = get_cols(year)

    # de-alias each language
    lang1 = sanitize(lang1, year)
    lang2 = sanitize(lang2, year)

    csvpath = get_survey_path(year)

    # groovy, haskell, elixir
    lang1lower = lang1.lower()
    lang2lower = lang2.lower()

    numlang1 = 0
    numcontinuelang1 = 0
    numlang2 = 0
    numcontinuelang2 = 0
    numboth = 0
    numpreferlang2 = 0
    numpreferlang1 = 0
    numnopref = 0
    # is there another language the person has used and wants to continue using, in
    # favour of lang1 and lang2?
    trump: Dict[str, int] = defaultdict(int)

    total = 0
    with csvpath.open() as f:
        reader = csv.reader(f)
        first = None
        for row in reader:
            total += 1
            if ((total % 1000) == 0):
                print('.', end='', flush=True)

            if first is None:
                first = row
                haveidx = row.index(usedcol)
                wantidx = row.index(wantcol)
                continue

            have = {lang.lower().strip() for lang in row[haveidx].split(';')}
            want = {lang.lower().strip() for lang in row[wantidx].split(';')}

            check = 0

            wantlang1 = lang1lower in want
            wantlang2 = lang2lower in want

            if lang2lower in have:
                check += 1
                numlang2 += 1
                if wantlang2:
                    numcontinuelang2 += 1

            if lang1lower in have:
                check += 1
                numlang1 += 1
                if wantlang1:
                    numcontinuelang1 += 1

            if check > 1:
                numboth += 1

                if wantlang1:
                    if wantlang2:
                        numnopref += 1
                    else:
                        numpreferlang1 += 1
                elif wantlang2:
                    numpreferlang2 += 1
                else:
                    for wanted in want:
                        if wanted in have:
                            trump[wanted] += 1

    # how many users don't want to use either any more?
    numstop = numboth - numpreferlang1 - numpreferlang2 - numnopref

    pccontinuelang1 = (100 * (float(numcontinuelang1) / float(numlang1))) if numlang1 else 0
    pccontinuelang2 = (100 * (float(numcontinuelang2) / float(numlang2))) if numlang2 else 0

    def q(num: int, total: int) -> str:
        pc = 100 * float(num) / float(total)
        return f"{num: 6d} ({pc:2.1f}%)"

    print('')
    print(f'Of {total} responses:')
    print(
        f'  {numlang1: 6d} have used {lang1}'
        f'; {numcontinuelang1} ({pccontinuelang1:.1f}%) wish to continue using it'
    )
    print(
        f'  {numlang2: 6d} have used {lang2}'
        f'; {numcontinuelang2} ({pccontinuelang2:.1f}%) wish to continue using it',
    )
    print(f'  {numboth: 6d} have used both')
    print(f'Of {numboth} respondends that have used both:')
    print(f'  {q(numpreferlang2, numboth)} want to continue using {lang2}, but not {lang1}')
    print(f'  {q(numpreferlang1, numboth)} want to continue using {lang1}, but not {lang2}')
    print(f'  {q(numnopref,      numboth)} want to continue using both')
    print(f"  {q(numstop,        numboth)} don't want to continue using either")

    # ignore 'SQL' as an alternative language
    trump.pop('sql', None)

    if alt:
        trumpitems = [(k, v) for k, v in trump.items() if v > 10]

        trumpitems.sort(key=lambda i: i[1], reverse=True)

        if len(trumpitems):
            print('  Popular alternatives:')
            for other, numother in trumpitems:
                print(f'    {numother} have also used {other} and want to use it instead')


@click.command()
@click.option('--dest', required=True)
@click.option('--title')
@click.argument('lang', nargs=2)
def render_fight(dest: str, lang: Tuple[str, str], title: Optional[str]) -> None:
    from stackwar.renderhtml import dump_fight
    from stackwar.languages import langtitle

    assert dest.endswith('.html'), "DEST must end in '.html'"

    yeardata = []

    only1 = 'Only ' + langtitle(lang[0])
    only2 = 'Only ' + langtitle(lang[1])

    _order = {
        only1: 1,
        'Both': 2,
        only2: 3,
        'Neither': 4,
    }

    swap_hues = False
    if sorted([only1, only2])[0] == only1:
        swap_hues = True

    for year in DOWNLOAD_LINKS.keys():
        lang1 = mostly_sanitize(lang[0], year)
        lang2 = mostly_sanitize(lang[1], year)

        yeartotal = 0

        def _item(state: str) -> None:
            nonlocal yeartotal
            yeartotal += 1
            yeardata.append({
                'year': year,
                'state': state,
                'tally': 1,
                'order': _order[state],
            })

        if not lang1:
            for used, want in iter_squashed(year):
                if lang2 in used:
                    _item(only2 if lang2 in want else 'Neither')
        elif not lang2:
            for used, want in iter_squashed(year):
                if lang1 in used:
                    _item(only1 if lang1 in want else 'Neither')
        else:
            for used, want in iter_squashed(year):
                if not (lang1 in used and lang2 in used):
                    continue

                if lang1 in want:
                    if lang2 in want:
                        _item('Both')
                    else:
                        _item(only1)
                elif lang2 in want:
                    _item(only2)
                else:
                    _item('Neither')

        if yeartotal < 1000:
            click.secho(f"Only {yeartotal} data points for {year}", fg="red")

    dump_fight(
        Path(dest),
        yeardata,
        lang1=lang[0],
        lang2=lang[1],
        swap_hues=swap_hues,
        title=title,
    )
