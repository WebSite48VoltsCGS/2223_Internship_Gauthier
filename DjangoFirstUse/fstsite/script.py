# Importation list

import pylatex
import os
import django

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

bid = Doc(documentclass='article', lmodern=False, textcomp=False, geometry_options="a4paper")
preamble = bid.preamble
adder = bid.preamble.append


for pack in packs:
    bid.packages.append(Pack(pack))


# Function definition

def V48(bid):
    adder(noEscape("\n"))
    adder(noEscape(r"\def\societe{48Volts}"))
    adder(noEscape(r"\def\adresseM{7 chemin des libellules ~-~ 95800"))
    adder(noEscape(r"\textsc{Courdimanche}}"))
    adder(noEscape(r"\def\adresse21{7 chemin des libellules \\ 95800"))
    adder(noEscape(r"\textsc{Courdimanche}}"))
    adder(noEscape(r"\def\capital{7 000 €}"))
    adder(noEscape(r"\def\gerant{Nicolas \textsc{Papazoglou}}"))
    adder(noEscape(r"\def\tel{06 09 28 15 36}"))
    adder(noEscape(r"\def\mail{nicolas.papazoglou@48-volts.fr}"))
    adder(noEscape(r"\def\contact{\gerant \\ Tel : \tel \\ Mail : \mail}"))
    adder(noEscape(r"\def\lieu{\textsc{Courdimanche}}"))
    adder(noEscape(r"\def\RCS{801 880 055 00018}"))
    adder(noEscape(r"\def\web{www.48-volts.fr}"))

def variable(bid):
    adder(noEscape("\n"))
    adder(noEscape(r"\def\TVA{20}"))
    adder(noEscape(r"\def\TotalHT{0}"))
    adder(noEscape(r"\def\ssTotalHT{0}"))
    adder(noEscape(r"\def\TotalTVA{0}"))
    adder(noEscape(r"\def\part_name{}"))
    adder(noEscape(r"\def\ListeProduits{}"))



client = Clients.objects.get(user_name="Hervé")
vente = Ventes.objects.get(id_client=client.id)


bid.append(noEscape(client))
bid.append(noEscape(vente))
for cmd in vente.id_commande.all():
    bid.append(cmd)

V48(bid)
variable(bid)


bid.generate_tex(filepath=r"D:\Git\Projet\2223_Internship_Gauthier\DjangoFirstUse\fstsite\devis\devis")
