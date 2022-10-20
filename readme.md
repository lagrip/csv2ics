# csv2ics
ICS file generator from csv file

Creates an ics file per calendar.

icsCreator.py is the same as csv2ics.py but with French prompts.
csv2ics.py is the latest version.

# Usage
## Requirements
- [Python](https://www.python.org/downloads/) 3.8+

## Instructions
1. Download csv2ics.py
2. Place the CSV Calendar in the same folder as the script.
3. Create a folder named ics.
4. Run the python script.
5. Wait for script to complete ("ICS files created successfully" in terminal).
6. ICS files are available in folder ics.

# CSV format
## Filename
`Calendar.csv`

Will throw `Error while opening Calendar.csv` if not found.

## Required columns
All column names must be present. This does not mean a field value is required (see table below). Leaving a required field empty may cause unexpected results.

Column order is not important.

Will throw `Error: Required columns missing in Calendar.csv` if a column is missing or misspelled.

| Name        | Required  | id    | Remarks                                        |
| ----------- | --------- | ----- | ---------------------------------------------- |
| Calendar    | **YES**   | `cal` | Calendar name                                  |
| Subject     | **YES**   | `sub` | Event title                                    |
| Start Date  | **YES**   | `sda` | Format `dd.mm.yyyy`                            |
| Start Time  | *depends* | `sti` | Format `hh:mm`. Ignored if 'All Day' is `TRUE` |
| End Date    | **YES**   | `eda` | Format `dd.mm.yyyy`                            |
| End Time    | *depends* | `eti` | Format `hh:mm`. Ignored if 'All Day' is `TRUE` |
| All Day     | no        | `day` | String `TRUE` if yes                           |
| Description | no        | `dsc` | Event details                                  |
| Location    | no        | `loc` | Event location                                 |
