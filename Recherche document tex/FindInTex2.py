# Files imported

import os

# Macro or variable definition

source = r"D:\Git\Projet\2223_Internship_Gauthier\Recherche document tex\Doc tex"

extraction = r"D:\Git\Projet\2223_Internship_Gauthier\Recherche document tex\Extraction2"


# Function definition

for file in os.listdir(source):
    if file.endswith(".tex"):
        path = os.path.join(source, file)
        path_ext = os.path.join(extraction, "extraction2.txt")
        with open(path_ext, "a", encoding="utf-8") as txt:
            with open(path, "r", encoding="utf-8") as tex:
                for line in tex:
                    if line.startswith(r"\def\ClientNom"):
                        txt.write(line)
                    if line.startswith(r"\def\ClientAdresse"):
                        txt.write(line)
        tex.close()
        txt.close()





# Class definition