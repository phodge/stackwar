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

## Other Commands

**bin/print-languages**

Print a list of languages for the given year's survey.
