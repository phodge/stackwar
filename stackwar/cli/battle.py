import csv
from collections import defaultdict
from typing import Dict

import click

from stackwar import get_survey_path
from stackwar.cli.utils import sanitize
from stackwar.surveyutils import get_cols


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
