# Importation list

import pylatex
import os
import django
import subprocess

os.environ['DJANGO_SETTINGS_MODULE'] = 'fstsite.settings'

django.setup()


from sql_test import models

# TODO

# Function calcul has been change, produits has been change. Need to rewrite the function to create the tabular, after
# that, just need to GET the value from devis.html (mostly figure out how I'll handle the discount part). Then it should
# be almost finished for the basic database and file generation. I'll need to put more validation things in the database
# but other than that, it should be ok to be migrated.

# Macros and variables definition

pylatex.base_classes.containers.Container.content_separator = '\n'

Doc = pylatex.Document
Pack = pylatex.Package
pageStyle = pylatex.PageStyle
noEscape = pylatex.NoEscape

Client = models.Client
Article = models.Article
Command = models.Command
Component = models.Component
CommandLine = models.CommandLine

packs = ["babel", "units", "bera", "graphicx", "fancyhdr", "fp", "longtable", "marvosym", "array", "multirow",
         "makecell", "datetime", "numprint"]

bid = Doc(documentclass='article', document_options=["11pt", "french"], lmodern=False,
          textcomp=False, geometry_options="a4paper")

adder = bid.append

preamble = bid.preamble
adderPreamble = bid.preamble.append

preamblePath = r"BasicTemplate\preamble.txt"
endPath = r"BasicTemplate\endfile.txt"
headerPath = r"BasicTemplate\introdoc.txt"
tabularPath = r"BasicTemplate\tabular.txt"


for pack in packs:
    bid.packages.append(Pack(pack))

client = Client.objects.get(user_name="Hervé")
command = Command.objects.get(client=client.id)

bidNumber = command.billing_id


cmdBash = r"pdflatex D:\Git\Projet\2223_Internship_Gauthier\fstsite\devis\devis.tex"

# Function definition

def better_round(x):
    if int(10*(100*x - int(100*x))) < 5:
        return round(x, 2)
    else:
        return round(x+0.01, 2)


def init_list():
    produits = []
    for commands in CommandLine.objects.filter(command=command.id):
        produit = [[f'{commands.article.product} {commands.article.description}', commands.article.category],
                  [[(article, int(Component.objects.get(kit=commands.article, article=article).number)),
                    [(art, int(Component.objects.get(kit=article, article=art).number))
                     for art in article.article.all()]] for article in commands.article.article.all()],
                  commands.number,
                  better_round(commands.article.buying_price),
                  0,
                  1,
                  0]
        produits.append(produit)

    return sorted(produits, key=lambda x: x[0][1])



def V48():
    # find a way to get: nomPrestation, lieuPrestation, debutPrestation, finPrestation, ClientNom, ClientAdresse
    # and add them to the doc

    address = client.adress.split(" ")
    adress1 = " ".join(address[:-2])
    adress2 = " ".join(address[-2:])

    if client.asso:
        name = client.name
    else:
        name = f'{client.user_name} {client.user_lastname}'

    deposit = 0

    not_yet = "A changer"

    adderPreamble(noEscape(f"\\def\\devisNum{{{bidNumber}}}"))
    adderPreamble(noEscape(f"\\def\\nomPrestation{{{not_yet}}}"))
    adderPreamble(noEscape(f"\\def\\lieuPrestation{{{not_yet}}}"))
    adderPreamble(noEscape(f"\\def\\debutPrestation{{{not_yet}}}"))
    adderPreamble(noEscape(f"\\def\\finPrestation{{{not_yet}}}"))

    adderPreamble(noEscape(f"\\def\\ClientNom{{{name}}}"))
    adderPreamble(noEscape(f"\\def\\Adressf{{{adress1}}}"))
    adderPreamble(noEscape(f"\\def\\Adresss{{{adress2}}}"))
    adderPreamble(noEscape(f"\\def\\deposit{{{f'{deposit:.2f}'}}}"))

    with open(preamblePath, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for line in lines:
        adderPreamble(noEscape(str(line.replace('\n', "", 1))))


def bank():
    with open(endPath, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for line in lines:
        adder(noEscape(str(line.replace('\n', "", 1))))


def header():
    with open(headerPath, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for line in lines:
        adder(noEscape(str(line.replace('\n', "", 1))))


def calcul(deposit):
    produits = init_list()
    TotalHT = 0
    TVA = 20

    j, ssTotalTable = 0, []

    for (i, produit) in enumerate(produits):
        total = produit[2]*produit[3]*produit[5]*(1-produit[4]/100)

        try:
            if produit[0][1] != produits[i][0][1]:
                j += 1
                ssTotalTable.append(total)
            else:
                ssTotalTable[j] += total
        except:
            ssTotalTable.append(total)

        TotalHT += total
        produit[6] = total

    TotalTVAToRound = TVA/100*TotalHT
    TotalTVA = better_round(TotalTVAToRound)
    Total = TotalHT + TotalTVA

    adderPreamble(noEscape(f"\\def\\TotalTVA{{{ f'{TotalTVA:.2f}' }}}"))
    adderPreamble(noEscape(f"\\def\\Total{{{ f'{Total:.2f}' }}}"))
    adderPreamble(noEscape(f"\\def\\TotalHT{{{ f'{TotalHT:.2f}' }}}"))
    adderPreamble(noEscape(f"\\def\\TVA{{{TVA}}}"))
    adderPreamble(noEscape(f"\\def\\totalLeft{{{ f'{Total - deposit:.2f}' }}}"))

    return produits, ssTotalTable, TotalTVA, TotalHT, TVA


def createTable(produits_final, ssTotalTable):
    j = 0
    mem = None
    with open(tabularPath, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for line in lines:
        if '%' in line:
            for produit in produits_final:
                if mem is None:
                    mem = produit[0][1]
                    adder(noEscape(f"\\textbf{{{mem}}} & & & & & \\\\"))
                elif mem != produit[0][1]:
                    adder(noEscape(f"Sous-total \\textbf{{{mem}}} & & & & & {f'{TotalTVA:.2f}'} \\\\"))
                    adder(noEscape(f" & & & & & \\\\"))
                    adder(noEscape(f"\\textbf{{{produit[0][1]}}} & & & & & \\\\"))
                    mem = produit[0][1]
                    j += 1

                adder(noEscape(
                    f"{produit[0][0]}& {produit[2]} & {f'{produit[3]:.2f}'} & {produit[4]}"
                    f" \% & {produit[5]} & {f'{produit[6]:.2f}'} \\\\"))
                if produit[1]:
                    for [(prod, nbr1), sub_prod] in produit[1]:
                        adder(noEscape(f"\\textit{{{prod}}} & {nbr1} & & & & \\\\"))
                        if sub_prod:
                            for (sub, nbr2) in sub_prod:
                                adder(noEscape(f"\\small\\textit{{{sub}}} & {nbr2} & & & & \\\\"))

            adder(noEscape(f"\\textbf{{Sous-total {mem}}} & & & & & {f'{ssTotalTable[j]:.2f}'}\\\\"))
            adder(noEscape(f' & & & & & \\\\'))

            adder(noEscape(f"\hline \hline"))
            adder(noEscape(f"Total HT & & & & & \TotalHT \\\\"))
            adder(noEscape(f"Total TVA (\TVA \%)  & & & & & \TotalTVA \\\\"))

            adder(noEscape(f"\hline \hline"))
            adder(noEscape(f"\\textbf{{Total TTC}} & & & & & \Total \\\\"))

        adder(noEscape(str(line.replace('\n', "", 1))))





def writing():
    deposit = 0

    produits_final, ssTotalTable, TotalTVA, TotalHT, TVA = calcul(deposit)

    # Preamble
    V48()

    # Header
    header()

    # Bid
    createTable(produits_final, ssTotalTable)

    # Bank
    bank()

    # Compilation
    bid.generate_tex(filepath=r"D:\Git\Projet\2223_Internship_Gauthier\fstsite\devis\devis")



    process = subprocess.Popen(cmdBash, shell=True,
                            cwd=r"D:\Git\Projet\2223_Internship_Gauthier\fstsite\devis",
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    process.communicate()


    process = subprocess.Popen(cmdBash, shell=True,
                            cwd=r"D:\Git\Projet\2223_Internship_Gauthier\fstsite\devis",
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    process.communicate()

writing()
