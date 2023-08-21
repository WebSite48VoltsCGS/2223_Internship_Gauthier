# Importation list

import pylatex
import os
import django
import subprocess

os.environ['DJANGO_SETTINGS_MODULE'] = 'fstsite.settings'

django.setup()


from sql_test import models



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



for pack in packs:
    bid.packages.append(Pack(pack))


produits = []       # list of list, 0 -> Article.product + Article.model
                    #               1 -> Commande.number
                    #               2 -> Article.buying_price
                    #               3 -> Article.discount default = 0
                    #               4 -> Commande.coeff default = 1
                    #               5 -> Total

client = Client.objects.get(user_name="Hervé")
command = Command.objects.get(client=client.id)

bidNumber = command.billing_id


cmdBash = r"pdflatex D:\Git\Projet\2223_Internship_Gauthier\fstsite\devis\devis.tex"

# Function definition


def init_list():
    for commands in CommandLine.objects.filter(command=command.id):
        produit = [f'{commands.article.product} {commands.article.brand} {commands.article.denomination}',
                   commands.number, commands.article.buying_price, 0, 1, 0]
        produits.append(produit)


def V48():
    # gérer l'acquisation de: nomPrestation, lieuPrestation, debutPrestation, finPrestation, ClientNom, ClientAdresse
    TotalTVA, TotalHT, ssTotalHT, TVA = calcul()

    deposit = None
    address = client.adress
    name = (client.user_name, client.user_lastname)

    adderPreamble(noEscape(f"\\def\\devisNum{{{bidNumber}}}"))
    adderPreamble(noEscape(f"\\def\\total{{{TotalTVA}}}"))
    if deposit is None:
        adderPreamble(noEscape(f"\\def\\deposit{{0}}"))
        adderPreamble(noEscape(f"\\def\\totalLeft{{{TotalTVA}}}"))
    else:
        adderPreamble(noEscape(f"\\def\\total{{{deposit}}}"))
        adderPreamble(noEscape(f"\\def\\totalLeft{{{TotalTVA - deposit}}}"))

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


def calcul():
    init_list()
    ssTotalHT = TotalHT = 0
    TVA = 20
    for produit in produits:
        total = produit[1]*produit[2]*produit[4]*(1-produit[3]/100)
        ssTotalHT += total
        TotalHT += total
        produit[5] = total
    TotalTVA = (1+TVA/100)*TotalHT
    return TotalTVA, TotalHT, ssTotalHT, TVA


def createTable():
    pass
def writing():
    # Preamble
    V48()

    # Header
    header()

    # Bid

    bid.append(noEscape(client))
    bid.append(noEscape(f'{command}\n'))
    for cmd in command.articles.all():
        adder(noEscape(f'{cmd}\n'))

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
