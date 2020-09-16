import csv
import sys

import click

from stackwar import DOWNLOAD_LINKS, get_squash_path, get_survey_path
from stackwar.surveyutils import get_cols


@click.command()
def squash() -> None:
    for year in DOWNLOAD_LINKS.keys():
        usedcol, wantcol = get_cols(year)

        collapse = {
            'visual basic': 'vb',
            'visual basic 6': 'vb',
            'vb.net': 'vb',
            'vba': 'vb',
        }
        if year == 2016:
            collapse.update({
                'android': 'java',
                'lamp': 'php',
                'node.js': 'javascript',
                'reactjs': 'javascript',
                'angularjs': 'javascript',
            })

        squashfile = get_squash_path(year)
        click.secho(f"Squashing {year} to {squashfile}", fg="yellow", err=True)

        csvpath = get_survey_path(year)

        with csvpath.open() as f_in, squashfile.open('w') as f_out:
            reader = csv.reader(f_in)
            writer = csv.writer(f_out)

            total = 0
            first = True
            for row in reader:
                total += 1
                if ((total % 1000) == 0):
                    sys.stderr.write('.')
                    sys.stderr.flush()

                if first:
                    first = False
                    usedidx = row.index(usedcol)
                    wantidx = row.index(wantcol)
                    continue

                used = {lang.lower().strip() for lang in row[usedidx].split(';')}
                want = {lang.lower().strip() for lang in row[wantidx].split(';')}

                # collapse some things
                for old, new in collapse.items():
                    if old in used:
                        used.remove(old)
                        used.add(new)
                    if old in want:
                        want.remove(old)
                        want.add(new)

                writer.writerow([
                    ":".join(used),
                    ":".join(want),
                ])

        sys.stderr.write("\n")
