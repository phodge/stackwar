import json
from pathlib import Path
from typing import Any, Dict, List

from stackwar.languages import langtitle

_TEMPLATE = """
<!DOCTYPE html>
<html>
  <head>
    <title>Chart</title>
    <meta charset="utf-8" />

    <script src="https://cdn.jsdelivr.net/npm/vega@5.12.1"></script>
    <script src="https://cdn.jsdelivr.net/npm/vega-lite@4.13.1"></script>
    <script src="https://cdn.jsdelivr.net/npm/vega-embed@6.8.0"></script>

    <style media="screen">
      /* Add space between Vega-Embed links  */
      .vega-actions a {
        margin-right: 5px;
      }
    </style>
  </head>
  <body>
    <h1>__TITLE__</h1>
    <!-- Container for the visualization -->
    <div id="vis"></div>

    <script>
      // Assign the specification to a local variable vlSpec.
      var vlSpec = __SPEC__;

      // Embed the visualization in the container with id `vis`
      vegaEmbed('#vis', vlSpec);
    </script>
  </body>
</html>"""


def _hsv2hex(h: int, s: float, v: float) -> str:
    import colorsys

    assert 0 <= h < 359

    r, g, b = colorsys.hsv_to_rgb(h / float(360), s, v)
    return '#{:02X}{:02X}{:02X}'.format(int(r * 255), int(g * 255), int(b * 255))


def dump_fight(
    dest: Path,
    values: List[Dict[str, Any]],
    *,
    title: str = None,
    lang1: str,
    lang2: str,
    swap_hues: bool,
) -> None:
    from stackwar.languages import get_hue

    spec = {
        '$schema': 'https://vega.github.io/schema/vega-lite/v4.json',
        'data': {
            'values': values,
        },
        'width': 800,
        'height': 400,
        'config': {
            'axis': {
                "labelFontSize": 20,
                "titleFontSize": 20,
                "titleFont": "Arial",
                "labelFont": "Arial",
            },
            'bar': {
                'discreteBandSize': 50,
                'continuousBandSize': 30,
            },
            'legend': {
                'labelLimit': 300,
            },
        },
    }

    spec['mark'] = {
        'type': 'bar',
        'cornerRadius': 5,
    }

    SAT = .65
    VVV = .80

    hue_lang1 = get_hue(lang1.lower())
    hue_lang2 = get_hue(lang2.lower())
    hue_both = int((hue_lang1 + hue_lang2) / 2)

    if swap_hues:
        hue_lang1, hue_lang2 = hue_lang2, hue_lang1

    spec['encoding'] = {
        'y': {
            "field": "tally",
            "type": "quantitative",
            "aggregate": "sum",
            "stack": "normalize",
            "axis": {
                "title": None,
            },
        },
        'x': {
            "field": "year",
            "type": "ordinal",
            "axis": {
                "title": "Year",
            },
        },
        'color': {
            "field": "state",
            "type": "nominal",
            "scale": {
                "range": [
                    _hsv2hex(hue_both, SAT, VVV),  # both
                    _hsv2hex(hue_both, 0, VVV),  # neither
                    _hsv2hex(hue_lang2, SAT, VVV),  # only lang2?
                    _hsv2hex(hue_lang1, SAT, VVV),  # only lang1
                ],
            },
            "legend": {
                #"labelFont": "Monospace",
                "labelFontSize": 20,
                "symbolStrokeWidth": 15,
                "title": "Devs want ...",
                "titleFontSize": 20,
            },
        },
        'order': {
            "field": 'order',
            "type": "quantitative",
        }
    }

    if title is None:
        title = f'{langtitle(lang1)} vs {langtitle(lang2)}'

    with dest.open('w') as f2:
        f2.write(_TEMPLATE.replace('__TITLE__', title).replace('__SPEC__', json.dumps(spec)))


def dump_chart(
    *,
    dest: Path,
    values: Any,
    title: str,
) -> None:
    spec = {
        '$schema': 'https://vega.github.io/schema/vega-lite/v4.json',
        'data': {
            'values': values,
        },
        'width': 800,
        'height': 400,
        'config': {
            'axis': {
                "labelFontSize": 20,
                "titleFontSize": 20,
                "titleFont": "Arial",
                "labelFont": "Arial",
            },
        },
        'mark': {'type': 'line'}
    }

    spec['transform'] = [
        {"calculate": "datum.love * 100", "as": "love100"},
    ]
    spec['encoding'] = {
        'x': {
            "field": "year",
            "type": "nominal",
            "axis": {
                "title": "Year",
            },
        },
        'y': {
            "field": "love100",
            "type": "quantitative",
            "scale": {"domain": [0, 100]},
            "axis": {
                "title": "Want to continue using (%)",
            },
        },
        'color': {
            "field": "lang",
            "type": "nominal",
            "legend": {
                "labelFont": "Monospace",
                "labelFontSize": 40,
                "symbolStrokeWidth": 15,
                "title": None,
            },
        },
    }

    with dest.open('w') as f2:
        f2.write(_TEMPLATE.replace('__TITLE__', title).replace('__SPEC__', json.dumps(spec)))
