from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
REPO_LOCAL = REPO_ROOT / '.local'


def get_survey_path(year: int) -> Path:
    ret = REPO_LOCAL / f'survey-results/{year}.csv'
    ret.parent.mkdir(parents=True, exist_ok=True)
    return ret


def get_squash_path(year: int) -> Path:
    ret = REPO_LOCAL / f'squashed/{year}.csv'
    ret.parent.mkdir(parents=True, exist_ok=True)
    return ret
