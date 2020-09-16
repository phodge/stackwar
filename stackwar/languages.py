from typing import Dict, Optional

from stackwar import REPO_ROOT

KEYFILE = REPO_ROOT / 'languages.yaml'
_HUES: Optional[Dict[str, int]] = None
_ALIASES: Optional[Dict[int, Dict[str, Optional[str]]]] = None
_BANS: Optional[Dict[str, str]] = None


def _get_hues() -> Dict[str, int]:
    global _HUES

    if _HUES is not None:
        return _HUES

    import yaml

    with KEYFILE.open() as f:
        data = yaml.safe_load(f)

    hues = data['hues']
    assert isinstance(hues, dict)
    _HUES = {x.lower(): hue for x, hue in hues.items()}
    assert all(isinstance(hue, int) for hue in hues.values())
    return _HUES


def _get_aliases() -> Dict[int, Dict[str, Optional[str]]]:
    global _ALIASES

    if _ALIASES is not None:
        return _ALIASES

    import yaml

    with KEYFILE.open() as f:
        data = yaml.safe_load(f)

    aliases = data['aliases']
    for key in aliases:
        assert isinstance(key, int)

    _ALIASES = aliases
    return _ALIASES


def _get_bans() -> Dict[str, str]:
    global _BANS

    if _BANS is not None:
        return _BANS

    import yaml

    with KEYFILE.open() as f:
        data = yaml.safe_load(f)

    bans = data['bans']
    for key, val in bans.items():
        assert isinstance(key, str)
        assert isinstance(val, str)

    _BANS = bans
    return _BANS


def unalias(lang: str, year: int) -> Optional[str]:
    return _get_aliases().get(year, {}).get(lang, lang)


def get_ban(lang: str) -> Optional[str]:
    return _get_bans().get(lang)


def is_known(lang: str) -> bool:
    return lang in _get_hues()
