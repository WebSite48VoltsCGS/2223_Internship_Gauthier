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

Clients = models.Client
Articles = models.Article
Ventes = models.Vente
Commandes = models.Commande

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


TVA = 20
TotalHT = 0
ssTotalHT = 0
TotalTVA = 0
produits = []       # list of list, 0 -> Article.product + Article.model
                    #               1 -> Commande.number
                    #               2 -> Article.buying_price
                    #               3 -> Article.discount default = 0
                    #               4 -> Commande.coeff default = 1
                    #               5 -> Total

client = Clients.objects.get(user_name="Hervé")
vente = Ventes.objects.get(id_client=client.id)

bidNumber = vente.id_bid


cmdBash = r"pdflatex D:\Git\Projet\2223_Internship_Gauthier\DjangoFirstUse\fstsite\devis\devis.tex"

# Function definition


def init_list():
    global produits
    for commands in vente.id_commande.all():
        produit = [commands.article.product + " " + commands.article.model + " " + commands.article.marque,
                   commands.number, commands.article.buying_price, 0, 1, 0]
        produits.append(produit)


def V48():
    # gérer l'acquisation de: nomPrestation, lieuPrestation, debutPrestation, finPrestation, ClientNom, ClientAdresse
    adderPreamble(noEscape(r"\def\devisNum{" + str(bidNumber) + "}"))
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
    global ssTotalHT, TotalHT, produits
    for produit in produits:
        total = produit[1]*produit[2]*produit[4]*(1-produit[3]/100)
        ssTotalHT += total
        TotalHT += total
        produit[5] = total


def createTable():
    global produits, ssTotalHT, TotalHT

def writing():
    # Preamble
    V48()

    # Header
    header()

    # Bid

    init_list()
    calcul()
    bid.append(noEscape(client))
    bid.append(noEscape(vente))
    for cmd in vente.id_commande.all():
        adder(cmd)

    # Bank
    bank()

    # Compilation
    bid.generate_tex(filepath=r"D:\Git\Projet\2223_Internship_Gauthier\DjangoFirstUse\fstsite\devis\devis")



    process = subprocess.Popen(cmdBash, shell=True,
                            cwd=r"D:\Git\Projet\2223_Internship_Gauthier\DjangoFirstUse\fstsite\devis",
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    process.communicate()


    process = subprocess.Popen(cmdBash, shell=True,
                            cwd=r"D:\Git\Projet\2223_Internship_Gauthier\DjangoFirstUse\fstsite\devis",
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    process.communicate()

# writing()
