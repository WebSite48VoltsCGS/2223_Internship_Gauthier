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

preamblePath = r"BasicTemplate\preamble.txt"
endPath = r"BasicTemplate\endfile.txt"
headerPath = r"BasicTemplate\introdoc.txt"
tabularPath = r"BasicTemplate\tabular.txt"


# Function definition

def better_round(x):
    if int(10*(100*x - int(100*x))) < 5:
        return round(x, 2)
    else:
        return round(x+0.01, 2)


def init_list(discount, coeff, bidId):
    produits = []
    commId = Command.objects.get(billing_id=bidId).id
    for (i, commands) in enumerate(CommandLine.objects.filter(command=commId)):
        produit = [[f'{commands.article.product} {commands.article.description}', commands.article.category],
                  [[(article, int(Component.objects.get(kit=commands.article, article=article).number)),
                    [(art, int(Component.objects.get(kit=article, article=art).number))
                     for art in article.article.all()]] for article in commands.article.article.all()],
                  commands.number,
                  better_round(commands.article.buying_price),
                  float(discount[i]),
                  float(coeff[i]),
                  0]
        produits.append(produit)

    return sorted(produits, key=lambda x: x[0][1])



def V48(bid, name, loc, deb, fin, deposit, bidId):
    # find a way to get: nomPrestation, lieuPrestation, debutPrestation, finPrestation, ClientNom, ClientAdresse
    # and add them to the doc

    client = Command.objects.get(billing_id=bidId).client

    address = client.adress.split(" ")
    adress1 = " ".join(address[:-2])
    adress2 = " ".join(address[-2:])

    if client.asso:
        name = client.name
    else:
        name = f'{client.user_name} {client.user_lastname}'

    bid.preamble.append(noEscape(f"\\def\\devisNum{{{bidId}}}"))
    bid.preamble.append(noEscape(f"\\def\\nomPrestation{{{name}}}"))
    bid.preamble.append(noEscape(f"\\def\\lieuPrestation{{{loc}}}"))
    bid.preamble.append(noEscape(f"\\def\\debutPrestation{{{deb}}}"))
    bid.preamble.append(noEscape(f"\\def\\finPrestation{{{fin}}}"))

    bid.preamble.append(noEscape(f"\\def\\ClientNom{{{name}}}"))
    bid.preamble.append(noEscape(f"\\def\\Adressf{{{adress1}}}"))
    bid.preamble.append(noEscape(f"\\def\\Adresss{{{adress2}}}"))
    bid.preamble.append(noEscape(f"\\def\\deposit{{{f'{deposit:.2f}'}}}"))

    with open(preamblePath, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for line in lines:
        bid.preamble.append(noEscape(str(line.replace('\n', "", 1))))


def bank(bid):
    with open(endPath, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for line in lines:
        bid.append(noEscape(str(line.replace('\n', "", 1))))


def header(bid):
    with open(headerPath, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for line in lines:
        bid.append(noEscape(str(line.replace('\n', "", 1))))


def calcul(bid, deposit, discount, coeff, bidId):
    produits = init_list(discount, coeff, bidId)
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

    bid.preamble.append(noEscape(f"\\def\\TotalTVA{{{ f'{TotalTVA:.2f}' }}}"))
    bid.preamble.append(noEscape(f"\\def\\Total{{{ f'{Total:.2f}' }}}"))
    bid.preamble.append(noEscape(f"\\def\\TotalHT{{{ f'{TotalHT:.2f}' }}}"))
    bid.preamble.append(noEscape(f"\\def\\TVA{{{TVA}}}"))
    bid.preamble.append(noEscape(f"\\def\\totalLeft{{{ f'{Total - float(deposit):.2f}' }}}"))

    return produits, ssTotalTable, TotalTVA, TotalHT, TVA


def createTable(bid, produits_final, ssTotalTable):
    j = 0
    mem = None
    with open(tabularPath, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for line in lines:
        if '%' in line:
            for produit in produits_final:
                if mem is None:
                    mem = produit[0][1]
                    bid.append(noEscape(f"\\textbf{{{mem}}} & & & & & \\\\"))
                elif mem != produit[0][1]:
                    bid.append(noEscape(f"Sous-total \\textbf{{{mem}}} & & & & & {f'{TotalTVA:.2f}'} \\\\"))
                    bid.append(noEscape(f" & & & & & \\\\"))
                    bid.append(noEscape(f"\\textbf{{{produit[0][1]}}} & & & & & \\\\"))
                    mem = produit[0][1]
                    j += 1

                article = produit[0][0].replace("&", r"\&").replace("$", r"\$")
                bid.append(noEscape(
                    f"{article}& {produit[2]} & {f'{produit[3]:.2f}'} & {produit[4]}"
                    f" \% & {produit[5]} & {f'{produit[6]:.2f}'} \\\\"))
                if produit[1]:
                    for [(prod, nbr1), sub_prod] in produit[1]:
                        bid.append(noEscape(f"\\textit{{ - {prod}}} & {nbr1} & & & & \\\\"))
                        if sub_prod:
                            for (sub, nbr2) in sub_prod:
                                bid.append(noEscape(f"\\small\\textit{{ • {sub}}} & {nbr2} & & & & \\\\"))

            bid.append(noEscape(f"\\textbf{{Sous-total {mem}}} & & & & & {f'{ssTotalTable[j]:.2f}'}\\\\"))
            bid.append(noEscape(f' & & & & & \\\\'))

            bid.append(noEscape(f"\hline \hline"))
            bid.append(noEscape(f"Total HT & & & & & \TotalHT \\\\"))
            bid.append(noEscape(f"Total TVA (\TVA \%)  & & & & & \TotalTVA \\\\"))

            bid.append(noEscape(f"\hline \hline"))
            bid.append(noEscape(f"\\textbf{{Total TTC}} & & & & & \Total \\\\"))

        bid.append(noEscape(str(line.replace('\n', "", 1))))





def writing(name, loc, deb, fin, deposit, discount, coeff, bidId):

    bid = Doc(documentclass='article', document_options=["11pt", "french"], lmodern=False,
              textcomp=False, geometry_options="a4paper")

    for pack in packs:
        bid.packages.append(Pack(pack))

    cmdBash = f"pdflatex D:\\Git\Projet\\2223_Internship_Gauthier\\fstsite\\devis\\devis_{bidId}.tex"

    produits_final, ssTotalTable, TotalTVA, TotalHT, TVA = calcul(bid, deposit, discount, coeff, bidId)

    # Preamble
    V48(bid, name, loc, deb, fin, float(deposit), bidId)

    # Header
    header(bid)

    # Bid
    createTable(bid, produits_final, ssTotalTable)

    # Bank
    bank(bid)

    # Compilation
    bid.generate_tex(filepath=f"D:\\Git\\Projet\\2223_Internship_Gauthier\\fstsite\\devis\\devis_{bidId}")



    process = subprocess.Popen(cmdBash, shell=True,
                            cwd=r"D:\Git\Projet\2223_Internship_Gauthier\fstsite\devis",
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    process.communicate()


    process = subprocess.Popen(cmdBash, shell=True,
                            cwd=r"D:\Git\Projet\2223_Internship_Gauthier\fstsite\devis",
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    process.communicate()

    bid = None
