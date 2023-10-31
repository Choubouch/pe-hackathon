# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.15.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# # Sujet 3 : les exoplanètes

# +
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import utility as util
# -

# ## Nettoyage des bases de données

# +
tcp = pd.read_csv('tess_confirmed_planet.csv', skiprows=99)

# Renommage des colonnes
assoc = util.get_rename_assoc('tess_confirmed_planet.csv')
tcp.rename(columns=assoc, inplace=True)

# On regarde le nombre d'enregistrements dans la base de données
# On vérifie que la première colonne peut constituer un index
print(tcp.shape[0] == len(tcp['Planet Name'].unique())) # := True

# Mise à jour de l'index
tcp.set_index('Planet Name', inplace=True)

# Retrait des colonnes inutiles
to_drop = ['Planetary Parameter Reference', 'Stellar Parameter Reference', 'Default Parameter Set', 'Controversial Flag', 'Stellar Metallicity Ratio']
tcp.drop(to_drop, axis=1, inplace=True)
# -

# On commence par importer les données. Ici ce sont les planètes qui ont été identifiées par le telescope TESS comme étant d'éventuelles exoplanètes, mais non prouvé
# Ensuite on selectionne les colonnes avec des données pertinentes, et qui sont communes aux autres tables pour pouvoir comparer. L'idée est de pouvoir faire des tracés communs avec les tables qui continnent les exoplanètes prouvées pour voire si les exoplanètes éventuelles sont pertinentes

tp = pd.read_csv('tess_project_candidates.csv', skiprows = 69)
assoc = util.get_rename_assoc('tess_project_candidates.csv')
tp.rename(columns=assoc, inplace=True)
tp = tp[['TESS Object of Interest','TESS Input Catalog ID','RA [sexagesimal]','Dec [sexagesimal]','Planet Orbital Period Value [days]','Planet Radius Value [R_Earth]','Planet Insolation Value [Earth flux]','Planet Equilibrium Temperature Value [K]','Stellar Distance [pc]','Stellar Effective Temperature Value [K]','Stellar Radius Value [R_Sun]']]
tp.set_index('TESS Object of Interest', inplace = True)
tp.dropna(how = 'any', inplace = True)

# ## Traitement des données


