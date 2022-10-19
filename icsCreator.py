import csv
from datetime import datetime, timedelta
import os

print("CREATEURS DE FICHIERS ICS DEPUIS CALENDRIER")
print("FAIT POUR LE SDIS COEUR DE LAVAUX")
print("(c) MARTIJN SASSEN")
print("Contact: it@msassen.ch")
print("17.12.2021 v1.5")
print("===========================================\n")

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

# open and read file
print('Ouverture du fichier Calendrier.csv...')
try:
    csvFile = open('Calendrier.csv', encoding='utf-8-sig')
    data = csv.DictReader(csvFile)
except:
    print("Erreur lors de l'ouverture du fichier Calendrier.csv")
    print("Vérifier la présence dudit fichier et de la dénomination correcte\n")
    os.system('pause')
    exit()

print("Fichier Calendrier.csv ouvert")

if not all (k in data.fieldnames for k in cols.values()):
    print("Erreur : Il manque des colonnes dans le fichier Calendrier.csv")
    print("Vous avez : " + ', '.join(data.fieldnames))
    print("Il faut :   " + ', '.join(cols.values()))
    print("L'ordre n'est pas important\n")
    os.system('pause')
    exit()

# sort events
print("Tri des événements...")
for row in data:
    try:
        calName = row[cols["cal"]]
        if calName not in c:
            c[calName] = []
        c[calName].append(row)
    except:
        csvFile.close()
        print("Erreur lors du tri des événements")
        os.system('pause')
        exit()
print("Evénements triés")

print("Création des fichiers ics...")
# create ics files
for key, events in c.items():
    f = open('ics/'+key+'.ics', "w", encoding='utf-8', newline='\n')
    # file header
    f.write('BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//MSASSEN\nCALSCALE:GREGORIAN\n\n')
    eCounter = 0

    for e in events:
        # event header
        f.write('BEGIN:VEVENT\n')

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
        f.write('DESCRIPTION:' + e[cols["dsc"]] + '\n')
        
        # event footer
        f.write('END:VEVENT\n\n')
        eCounter += 1

    # file footer
    f.write('END:VCALENDAR')
    f.close()

    # end of file
    totalEvents += eCounter
    fCounter += 1
    print(f'Fichier {key}.ics crée : {eCounter} événement(s)')

print('Fermeture du fichier Calendrier.csv...')
csvFile.close()
print("Fichier Calendrier.csv fermé")

print('Creation des fichiers ics terminée avec succès')
print(f'{fCounter} fichiers crées avec un total de {totalEvents} événement(s)')
print()
os.system('pause')