from pathlib import Path

DOWNLOAD_LINKS = {
    2016: 'https://drive.google.com/uc?export=download&id=0B0DL28AqnGsrV0VldnVIT1hyb0E',
    2017: 'https://drive.google.com/uc?export=download&id=0B6ZlG_Eygdj-c1kzcmUxN05VUXM',
    2018: 'https://drive.google.com/uc?export=download&id=1_9On2-nsBQIw3JiY43sWbrF8EjrqrR4U',
    2019: 'https://drive.google.com/uc?export=download&id=1QOmVDpd8hcVYqqUXDXf68UMDWQZP0wQV',
    2020: 'https://drive.google.com/uc?export=download&id=1dfGerWeWkcyQ9GX9x20rdSGj7WtEpzBB',
}

REPO_ROOT = Path(__file__).parent.parent
REPO_LOCAL = REPO_ROOT / '.local'


def get_zip_path(year: int) -> Path:
    ret = REPO_LOCAL / f'survey-zips/{year}.zip'
    ret.parent.mkdir(parents=True, exist_ok=True)
    return ret


def get_survey_path(year: int) -> Path:
    ret = REPO_LOCAL / f'survey-results/{year}.csv'
    ret.parent.mkdir(parents=True, exist_ok=True)
    return ret


def get_squash_path(year: int) -> Path:
    ret = REPO_LOCAL / f'squashed/{year}.csv'
    ret.parent.mkdir(parents=True, exist_ok=True)
    return ret
