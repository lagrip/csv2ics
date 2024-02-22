import csv
from datetime import datetime, timedelta, timezone
import os
import textwrap

print("CSV2ICS")
print("Licence: GPL-3.0")
print("22.02.2024 v1.5.1")
print("================\n")

c = {}  # Dict containing all calendars
cols = {
    "cal": "Calendar",
    "sub": "Subject",
    "sda": "Start Date",
    "sti": "Start Time",
    "eda": "End Date",
    "eti": "End Time",
    "day": "All Day",
    "dsc": "Description",
    "loc": "Location"
}
totalEvents = 0
fCounter = 0  # Counter for ics files created
now = datetime.now(timezone.utc)
nowical = now.strftime('%Y%m%dT%H%M%SZ')

# open and read file
print('Opening Calendar.csv...')
try:
    csvFile = open('Calendar.csv', encoding='utf-8-sig')
    data = csv.DictReader(csvFile)
except:
    print("Error while opening Calendar.csv")
    print("Check the file is present and has the right name\n")
    os.system('pause')
    exit()

print("Calendar.csv opened")

if not all (k in data.fieldnames for k in cols.values()):
    print("Error: Required columns missing in Calendar.csv")
    print("You have: " + ', '.join(data.fieldnames))
    print("You need: " + ', '.join(cols.values()))
    print("The order is not important\n")
    os.system('pause')
    exit()

# sort events (create calendars)
print("Sorting events...")
for row in data:
    try:
        calName = row[cols["cal"]]
        if calName not in c:
            c[calName] = []
        c[calName].append(row)
    except:
        csvFile.close()
        print("Error while sorting events\n")
        os.system('pause')
        exit()
print("Events sorted")

print("Creating ics files...")
# create ics files
for key, events in c.items():
    f = open('ics/'+key+'.ics', "w", encoding='utf-8')
    # file header
    f.write('BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//MSASSEN//CSV2ICS//EXPORT\nCALSCALE:GREGORIAN\n')
    eCounter = 0

    for e in events:
        # event header
        f.write('BEGIN:VEVENT\n')
        f.write('DTSTAMP:' + nowical + '\n')
        f.write(f'UID:CdL-{nowical}F{fCounter}E{eCounter}\n')

        # event data
        if e[cols["day"]] == "TRUE":
            start = datetime.strptime(e[cols["sda"]], '%d.%m.%Y')
            end = datetime.strptime(e[cols["eda"]], '%d.%m.%Y') + timedelta(days=1)
            f.write('DTSTART;VALUE=DATE:' + start.strftime('%Y%m%d') + '\n')
            f.write('DTEND;VALUE=DATE:' + end.strftime('%Y%m%d') + '\n')
        else:
            start = datetime.strptime(e[cols["sda"]]+' '+e[cols["sti"]], '%d.%m.%Y %H:%M')
            end = datetime.strptime(e[cols["eda"]]+' '+e[cols["eti"]], '%d.%m.%Y %H:%M')
            f.write('DTSTART:' + start.strftime('%Y%m%dT%H%M%S') + '\n')
            f.write('DTEND:' + end.strftime('%Y%m%dT%H%M%S') + '\n')

        f.write('SUMMARY:' + e[cols["sub"]] + '\n')
        f.write('LOCATION:' + e[cols["loc"]] + '\n')
        f.write('STATUS:CONFIRMED' + '\n')
        f.write('DESCRIPTION:' + '\n '.join(textwrap.wrap(e[cols["dsc"]], width=60)) + '\n')
        
        # event footer
        f.write('END:VEVENT\n')
        eCounter += 1

    # file footer
    f.write('END:VCALENDAR')
    f.close()

    # end of file
    totalEvents += eCounter
    fCounter += 1
    print(f'{key}.ics created: {eCounter} event(s)')

print('Closing Calendar.csv...')
csvFile.close()
print("Calendar.csv closed")

print('ICS files created successfully')
print(f'{fCounter} files created for a total of {totalEvents} event(s)')
print()
os.system('pause')