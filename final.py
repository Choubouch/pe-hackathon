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

k2 = pd.read_csv('k2_planets_and_candidates.csv', skiprows = 98)
assoc = util.get_rename_assoc('k2_planets_and_candidates.csv')
k2.rename(columns=assoc, inplace=True)
k2.drop(['Default Parameter Set','Planetary Parameter Reference','System Parameter Reference',
       'Archive Disposition', 'Archive Disposition Reference', 'Discovery Method', 'Discovery Facility', 'Solution Type',
       'Controversial Flag',
       'Orbital Period Upper Unc. [days]', 'Orbital Period Lower Unc. [days]',
       'Orbital Period Limit Flag', 'Orbit Semi-Major Axis [au])',
       'Orbit Semi-Major Axis Upper Unc. [au]',
       'Orbit Semi-Major Axis Lower Unc. [au]',
       'Orbit Semi-Major Axis Limit Flag', 'Planet Radius Upper Unc. [Earth Radius]',
       'Planet Radius Lower Unc. [Earth Radius]', 'Planet Radius Limit Flag',
       'Planet Radius Upper Unc. [Jupiter Radius]',
       'Planet Radius Lower Unc. [Jupiter Radius]', 'Planet Radius Limit Flag',
       'Planet Mass or Mass*sin(i) [Earth Mass]',
       'Planet Mass or Mass*sin(i) [Earth Mass] Upper Unc.',
       'Planet Mass or Mass*sin(i) [Earth Mass] Lower Unc.',
       'Planet Mass or Mass*sin(i) [Earth Mass] Limit Flag',
       'Planet Mass or Mass*sin(i) [Jupiter Mass]',
       'Planet Mass or Mass*sin(i) [Jupiter Mass] Upper Unc.',
       'Planet Mass or Mass*sin(i) [Jupiter Mass] Lower Unc.',
       'Planet Mass or Mass*sin(i) [Jupiter Mass] Limit Flag',
       'Planet Mass or Mass*sin(i) Provenance', 'Eccentricity',
       'Eccentricity Upper Unc.', 'Eccentricity Lower Unc.',
       'Eccentricity Limit Flag',
       'Insolation Flux Upper Unc. [Earth Flux]',
       'Insolation Flux Lower Unc. [Earth Flux]', 'Insolation Flux Limit Flag',
       'Equilibrium Temperature Upper Unc. [K]',
       'Equilibrium Temperature Lower Unc. [K]',
       'Equilibrium Temperature Limit Flag',
       'Data show Transit Timing Variations', 'Spectral Type',
       'Stellar Effective Temperature Upper Unc. [K]',
       'Stellar Effective Temperature Lower Unc. [K]',
       'Stellar Effective Temperature Limit Flag',
       'Stellar Radius Upper Unc. [Solar Radius]',
       'Stellar Radius Lower Unc. [Solar Radius]', 'Stellar Radius Limit Flag',
       'Stellar Mass [Solar mass]', 'Stellar Mass Upper Unc. [Solar mass]',
       'Stellar Mass Lower Unc. [Solar mass]', 'Stellar Mass Limit Flag',
       'Stellar Metallicity [dex]', 'Stellar Metallicity Upper Unc. [dex]',
       'Stellar Metallicity Lower Unc. [dex]',
       'Stellar Metallicity Limit Flag', 'Stellar Metallicity Ratio',
       'Stellar Surface Gravity Upper Unc. [log10(cm/s**2)]',
       'Stellar Surface Gravity Lower Unc. [log10(cm/s**2)]',
       'Stellar Surface Gravity Limit Flag', 'RA [sexagesimal]', 'RA [deg]',
       'Dec [sexagesimal]', 'Dec [deg]',
       'Distance [pc] Upper Unc', 'Distance [pc] Lower Unc',
       'V (Johnson) Magnitude Upper Unc',
       'V (Johnson) Magnitude Lower Unc', 
       'Ks (2MASS) Magnitude Upper Unc', 'Ks (2MASS) Magnitude Lower Unc',
       'Gaia Magnitude Upper Unc',
       'Gaia Magnitude Lower Unc',
       'Planetary Parameter Reference Publication Date'],axis=1,inplace=True)  
#je supprime les colonnes contenant n'ayant pas des données intéressantes

df_brut = pd.read_csv("confirmed_planets.csv", skiprows = 96)
assoc = util.get_rename_assoc("confirmed_planets.csv")
df_brut.rename(columns=assoc, inplace=True)
df_brut.columns

cp = df_brut.drop(['Date of Last Update', 'Controversial Flag', 'Spectral Type', 'Stellar Parameter Reference',
                  'Stellar Metallicity [dex]', 'Stellar Metallicity Upper Unc. [dex]', 'Stellar Metallicity Lower Unc. [dex]',
                  'Stellar Metallicity Limit Flag', 'Stellar Metallicity Ratio', 'Release Date'], axis = 1)


# Je supprime un certain nombre de colonnes dont je sais que je ne me servirai pas par la suite. Je vais ensuite créer des DataFrames qui me seront utiles par la suite.

df_disc = cp[['Planet Name', 'Host Name', 'Number of Planets', 'Discovery Method', 'Discovery Year', 'Discovery Facility', 'Planet Radius [Earth Radius]', 'Distance [pc]'  ]]
df_disc.rename(columns={'Discovery Year' : 'Discovery_Year'}, inplace=True)
df_ti = cp[['Planet Name','Equilibrium Temperature [K]', 'Insolation Flux [Earth Flux]']]
df_ti = df_ti.drop_duplicates()
df_ti = df_ti.dropna()
df_eff = cp[['Planet Name', 'Discovery Method']]
df_eff = df_eff.drop_duplicates()
group = df_eff.groupby(by = 'Discovery Method')
df_Teq = cp[['Planet Name', 'Equilibrium Temperature [K]']]
df_Teq = df_Teq.drop_duplicates()
df_Teq = df_Teq.dropna()

# ## Traitement des données

# #### Nombre de découverte en fonction de l'année

tcp.hist('Discovery Year', bins=50);

# #### Répartition des rayons des planètes

tcp.hist('Planet Radius [Earth Radius]', bins=50);

# #### Répartition des masses des planètes

tcp.hist('Planet Mass or Mass*sin(i) [Earth Mass]', bins=50);

# #### Répartition des températures d'équilibre

tcp.hist('Equilibrium Temperature [K]', bins=50);

# #### Corrélation entre température de la planète et insolation

tcp.plot.scatter(y='Equilibrium Temperature [K]', x='Insolation Flux [Earth Flux]');

# #### Corrélation entre température de la planète et température de son étoile

tcp.plot.scatter(y='Equilibrium Temperature [K]', x='Stellar Effective Temperature [K]');

# #### Corrélation entre période de rotation et rayon de la planète

tcp.plot.scatter(y='Orbital Period [days]', x='Planet Radius [Earth Radius]');

# #### Corrélation du rayon des planètes en fonction de la température d'équilibre

tcp.plot.scatter(x='Equilibrium Temperature [K]', y='Planet Radius [Earth Radius]');

# #### Lien entre rayon des planètes et température d'équilibre en fonction de l'année

sns.relplot(data=tcp, x='Distance [pc]', y='Stellar Radius [Solar Radius]', hue='Discovery Year');

# #### Lien entre température des planètes et de leur étoile en fonction de l'insolation des étoiles

sns.relplot(data=tcp, x='Stellar Effective Temperature [K]', hue='Insolation Flux [Earth Flux]', y='Equilibrium Temperature [K]');


