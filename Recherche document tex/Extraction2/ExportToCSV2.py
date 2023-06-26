# Importation list

import csv

# Macro and variable definition

extract = "extraction2.txt"
docCSV = "extraction2.csv"


# Function definition

def delDef():
    with open(extract, "r", encoding="utf-8") as file:
        lines = file.readlines()
    file.close()

    with open(docCSV, "w", encoding="utf-8", newline='') as fileCSV:
        writer = csv.writer(fileCSV, delimiter=';')
        newlines = []
        for line in lines:
            line = line.replace("\def\ClientAdresse", "", 1)
            line = line.replace("\def\ClientNom", "", 1)
            line = line.replace("}", ";")
            line = line.replace("{", "")
            newlines.append(line)

        finalLines = []
        for i in range(0, len(newlines), 2):
            finalLines.append(newlines[i] + newlines[i+1])


        finalLines = list(set(finalLines))
        finalLines.sort()

        for line in finalLines:
            line = line.split(";")
            writer.writerow(line)

    fileCSV.close()


delDef()

# Class definition