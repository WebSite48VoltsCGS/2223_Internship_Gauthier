# Importation list

import csv

# Macro and variable definition

extract = "extraction.txt"
docCSV = "extraction.csv"


# Function definition

def delProduit():
    with open(extract, "r", encoding="utf-8") as file:
        lines = file.readlines()
    file.close()

    with open(docCSV, "w", encoding="utf-8", newline='') as fileCSV:
        writer = csv.writer(fileCSV, delimiter=';')
        newlines = []
        for line in lines:
            if line.startswith("\\Produit{"):
                line = line.replace("\\Produit{", "", 1)
            elif line.startswith("\\ProduitNP{"):
                line = line.replace("\\ProduitNP{", "", 1)
            line = line.replace("}", ";")
            line = line.replace("{", "")
            newlines.append(line)

        newlines = list(set(newlines))
        newlines.sort()

        dic = {}
        for line in newlines:
            columns = line.split(';')
            key = columns[0]
            if key not in dic and key != "":
                dic[key] = columns

        newlines = list(dic.values())

        for line in newlines:
            writer.writerow(line)

    fileCSV.close()


delProduit()

# Class definition
