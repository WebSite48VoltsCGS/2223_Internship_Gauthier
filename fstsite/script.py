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


def init_list():
    produits = []
    for commands in CommandLine.objects.filter(command=command.id):
        produit = [[f'{commands.article.product} {commands.article.description}', commands.article.category],
                  [[article, [art for art in article.article.all()]] for article in commands.article.article.all()],
                  commands.number,
                  commands.article.buying_price,
                  0,
                  1,
                  0]
        produits.append(produit)

    return sorted(produits, key=lambda x: x[0][1])


def V48():
    # find a way to get: nomPrestation, lieuPrestation, debutPrestation, finPrestation, ClientNom, ClientAdresse
    # and add them to the doc
    address = client.adress
    name = (client.user_name, client.user_lastname)
    deposit = 0

    adderPreamble(noEscape(f"\\def\\devisNum{{{bidNumber}}}"))
    adderPreamble(noEscape(f"\\def\\deposit{{{deposit}}}"))

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
    ssTotalHT = TotalHT = 0
    TVA = 20
    for produit in produits:
        total = produit[2]*produit[3]*produit[5]*(1-produit[4]/100)
        ssTotalHT += total
        TotalHT += total
        produit[6] = total

    TotalTVA = TVA/100*TotalHT
    Total = TotalHT + TotalTVA

    adderPreamble(noEscape(f"\\def\\TotalTVA{{{TotalTVA}}}"))
    adderPreamble(noEscape(f"\\def\\Total{{{Total}}}"))
    adderPreamble(noEscape(f"\\def\\TotalHT{{{TotalHT}}}"))
    adderPreamble(noEscape(f"\\def\\ssTotalHT{{{ssTotalHT}}}"))
    adderPreamble(noEscape(f"\\def\\TVA{{{TVA}}}"))
    adderPreamble(noEscape(f"\\def\\totalLeft{{{Total - deposit}}}"))

    return produits, TotalTVA, TotalHT, ssTotalHT, TVA


def createTable(produits_final):
    bol = 1
    if bol:
        pass
    else:
        with open(tabularPath, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        for line in lines:
            if '%' in line:
                for produit in produits_final:
                    adder(noEscape(
                        f"\\text{{{produit[0]}}} & {produit[1]} & {produit[2]} \EUR & {produit[3]}"
                        f" \% & {produit[4]} & {produit[5]} \EUR \\\\"))

                adder(noEscape(f"\hline \hline"))
                adder(noEscape(r"Total HT & & & & & \totalHT \\"))
                adder(noEscape(r"Total TVA (\TVA) & & & & & \totalTVA \\"))

                adder(noEscape(r"\hline \hline"))
                adder(noEscape(r"\textbf{Total TTC} & & & & & \\total \\\\"))

            adder(noEscape(str(line.replace('\n', "", 1))))





def writing():
    deposit = 0

    produits_final, TotalTVA, TotalHT, ssTotalHT, TVA = calcul(deposit)

    # Preamble
    V48()

    # Header
    header()

    # Bid
    createTable(produits_final)


    bid.append(noEscape(client))
    bid.append(noEscape(f'{command}\n'))
    id_command = command.id
    for cmd in CommandLine.objects.filter(command=id_command):
        adder(noEscape(f'{cmd.article} {cmd.article.buying_price} x {cmd.number}\n'))
    # for cmd in command.articles.all():

    #    adder(noEscape(f'{cmd} {cmd.buying_price}\n'))

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
