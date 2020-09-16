import click

from stackwar import DOWNLOAD_LINKS, get_survey_path, get_zip_path


@click.command()
@click.option('--replace', is_flag=True)
def download_all(replace: bool) -> None:
    import requests
    from zipfile import ZipFile

    for year, link in DOWNLOAD_LINKS.items():
        zippath = get_zip_path(year)
        if zippath.exists():
            if replace:
                zippath.unlink()
            else:
                click.secho(f"{zippath} already exists", fg="cyan")
                continue

        click.secho(f"Downloading {year} data to {zippath}", fg="cyan")
        response = requests.get(link)
        response.raise_for_status()
        zippath.write_bytes(response.content)

    for year in DOWNLOAD_LINKS.keys():
        zippath = get_zip_path(year)
        csvpath = get_survey_path(year)
        click.secho(f"Extracting {year} survey data to {csvpath}", fg="cyan")

        if year == 2016:
            path = '2016 Stack Overflow Survey Results/2016 Stack Overflow Survey Responses.csv'
        else:
            path = 'survey_results_public.csv'

        with zippath.open('rb') as f_in, csvpath.open('wb') as f_out:
            f_out.write(ZipFile(f_in).read(path))
