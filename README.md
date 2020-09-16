# stackwar
Tools to compare language popularity using Stack Overflow survey data

## Setup

**bin/download-all**

Downloads the raw data for each year's survey (2016-2020).

**bin/squash**

Flattens raw survey data into a merged form that can be processed more quickly.

## Commands

**bin/battle-text**

Usage: `bin/battle-text -y YEAR LANG1 LANG2`

Show a text result of battling `LANG1` against `LANG2` using data from `YEAR`.

**bin/render-battle**

Usage: `bin/render-battle [OPTIONS] LANG LANG --dest=battle.html`

This will generate a file named "battle.html" which uses some 3rd party
libraries to display a chart showing how many developers prefer each of the
given languages over the last several years.


## Other Commands

**bin/print-languages**

Print a list of languages for the given year's survey.


**bin/lovedata**

Generate "lovedata" for the given languages and store it in a .json file.

E.g.:

* `bin/lovedata java kotlin > android.json`
* `bin/lovedata vba vb.net 'c#' > microsoft.json`
* `bin/lovedata swift objective-c > mac.json`
* `bin/lovedata php python java perl kotlin objective-c swift vb.net 'c#' c c++ ruby go rust > all.json`
* `bin/lovedata c c++ go rust > lowlevel.json`
* `bin/lovedata php python perl ruby > scripting.json`

**bin/renderlove**

Render the .json file from the previous step as a chart.
