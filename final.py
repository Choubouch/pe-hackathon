# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.15.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# # Sujet 3 : les exoplanètes

# +
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as ptch
import seaborn as sns

import utility as util
# -

# Nous avons trouvé 4 bases de données à exploiter. Elles contiennent les exoplanètes ou les candidats à être des exoplanètes. Deux proviennent du satellite TESS, une du satellite K2 et la dernière regroupe l'ensemble des exoplanètes confirmées.

# ## Nettoyage des bases de données
# > Pour faciliter la lecture, on n'utilisera qu'une seule cellule par base de données à nettoyer.
# > 
# > Évidemment, lors du développement, chaque opération était séparée dans une cellule.

# __Pour les exoplanètes trouvées par TESS :__

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

# Gestion du format de dates
tcp["Date of Last Update"] = pd.to_datetime(tcp["Date of Last Update"], format="%Y-%m-%d")
tcp["Planetary Parameter Reference Publication Date"] = pd.to_datetime(tcp["Planetary Parameter Reference Publication Date"], format="%Y-%m")
tcp["Release Date"] = pd.to_datetime(tcp["Release Date"], format="%Y-%m-%d")
# -

# __Pour les candidates à devenir des exoplanètes :__
#
# Ici ce sont les planètes qui ont été identifiées par le telescope TESS comme étant d'éventuelles exoplanètes, mais non prouvé.
#
# On ne selectionne que les colonnes avec des données pertinentes qui sont communes aux autres tables pour pouvoir comparer. L'idée est de pouvoir faire des tracés communs avec les tables qui contiennent les exoplanètes prouvées pour voire si les exoplanètes éventuelles sont pertinentes

# +
# On commence par importer les données
tp = pd.read_csv('tess_project_candidates.csv', skiprows = 69)

assoc = util.get_rename_assoc('tess_project_candidates.csv')
tp.rename(columns=assoc, inplace=True)

# On selectionne les colonnes avec des données pertinentes et
# qui sont communes aux autres tables pour pouvoir comparer
tp = tp[['TESS Object of Interest','TESS Input Catalog ID','RA [sexagesimal]','Dec [sexagesimal]','Planet Orbital Period Value [days]','Planet Radius Value [R_Earth]','Planet Insolation Value [Earth flux]','Planet Equilibrium Temperature Value [K]','Stellar Distance [pc]','Stellar Effective Temperature Value [K]','Stellar Radius Value [R_Sun]']]
tp.set_index('TESS Object of Interest', inplace = True)
tp.dropna(how = 'any', inplace = True)
# -

# __Pour le satellite K2 :__

# +
k2 = pd.read_csv('k2_planets_and_candidates.csv', skiprows = 98)

assoc = util.get_rename_assoc('k2_planets_and_candidates.csv')
k2.rename(columns=assoc, inplace=True)

# On supprime les colonnes ne contenant pas de données intéressantes
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
       'Planetary Parameter Reference Publication Date'], axis=1, inplace=True)

# Gestion du format de dates
# Certaines dates incluent une heure précise ... pour simplifier, on ignore cette heure.
k2["Release Date"] = k2["Release Date"].str.split(' ').str[0]

k2["Date of Last Update"] = pd.to_datetime(k2["Date of Last Update"], format="%Y-%m-%d")
k2["Release Date"] = pd.to_datetime(k2["Release Date"], format="%Y-%m-%d")
# -

# __Pour l'ensemble des exoplanètes :__

# +
df_brut = pd.read_csv("confirmed_planets.csv", skiprows=96)

assoc = util.get_rename_assoc("confirmed_planets.csv")
df_brut.rename(columns=assoc, inplace=True)

# On supprime un certain nombre de colonnes dont on ne sait pas quoi en faire par la suite 
cp = df_brut.drop(['Date of Last Update', 'Controversial Flag', 'Spectral Type', 'Stellar Parameter Reference',
                  'Stellar Metallicity [dex]', 'Stellar Metallicity Upper Unc. [dex]', 'Stellar Metallicity Lower Unc. [dex]',
                  'Stellar Metallicity Limit Flag', 'Stellar Metallicity Ratio', 'Release Date'], axis=1)
cp.rename(columns={'Discovery Year' : 'Discovery_Year'}, inplace=True)
cp.drop_duplicates(inplace=True)
cp.dropna(inplace=True)

# On crée ensuite des DataFrames qui nous seront utiles par la suite
df_disc = cp[['Planet Name', 'Host Name', 'Number of Planets', 'Discovery Method', 'Discovery_Year', 'Discovery Facility', 'Planet Radius [Earth Radius]', 'Distance [pc]'  ]]
df_ti = cp[['Planet Name','Equilibrium Temperature [K]', 'Insolation Flux [Earth Flux]']]
df_eff = cp[['Planet Name', 'Discovery Method']]
group = df_eff.groupby(by = 'Discovery Method')
df_Teq = cp[['Planet Name', 'Equilibrium Temperature [K]']]
# -

# ## Traitement des données

# #### Nombre de découvertes en fonction de l'année

# +
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Ici pour les exoplanètes découvertes par TESS
tcp.hist("Discovery Year", ax=axes[0])
axes[0].set_title("Exoplanètes découvertes par TESS")

# Ici pour les exoplanètes potentielles et effectivement découvertes par K2
k2.hist("Discovery Year", ax=axes[1]);
axes[1].set_title("Exoplanètes potentielles et effectivement\n découvertes par K2")

# Ici pour l'ensemble des exoplanètes confirmées
df_disc.hist("Discovery_Year", ax=axes[2])
plt.title("Ensemble des exoplanètes confirmées");

fig.suptitle("Nombre d'exoplanètes découvertes par année", y=1.05);
# -

# Les découvertes d'exoplanètes __augmentent avec le temps__, ce qui corrobore le __perfectionnement technique__ de ceux-ci avec le temps.
#
# On remarque cependant un pic de découvertes par le télescope K2 *(prolongation de la mission Kepler)* entre 2016 et 2018, avant une décroissance très rapide : la mission effective de ce téléscope s'est __achevée en 2019__.
#
# On remarque enfin qu'on découvre plus d'exoplanètes par an, qu'on en « valide » après analyse et observation plus précise.

# ***

# #### Répartition des rayons des planètes

# +
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Ici pour les exoplanètes découvertes par TESS
tcp.hist('Planet Radius [Earth Radius]', ax=axes[0], bins=50, range=[0, 25])
axes[0].set_title("Exoplanètes découvertes par TESS")

# Ici pour les exoplanètes éventuelles découvertes par TESS
tp['Planet Radius Value [R_Earth]'].hist(bins=50, ax=axes[1], range=[0, 25])
axes[1].set_title("Exoplanètes éventuelles découvertes par TESS")

# Ici pour les exoplanètes potentielles et effectivement découvertes par K2
k2['Planet Radius [Earth Radius]'].hist(bins=50, ax=axes[2], range=[0, 25])
axes[2].set_title("Exoplanètes potentielles et effectivement\n découvertes par K2")

fig.suptitle("Répartition des rayons des planètes\n[Unité de rayon de la Terre]", y=1.05);
# -

# On constate également qu'une grande partie des exoplanètes découvertes par TESS et K2 ont un rayon __du même ordre de grandeur__ que celui de la Terre *(entre 1 et 5 fois celui-ci)*.
#
# TESS détecte cependant __beaucoup d'exoplanètes de rayon plus important__ *(10 à 15 fois celui de la Terre)*. Ceci peut s'expliquer par __sa sensibilité photométrique ou sa résolution angulaire, plus grande__, lui permettant d'observer des objets plus lointains.

# ***

# #### Répartition des masses des planètes

# +
fig, axes = plt.subplots(1, 2, figsize=(10, 5))

# Ici pour les exoplanètes découvertes par TESS
mask = tcp["Planet Mass or Mass*sin(i) [Earth Mass]"] > 0
tcp[mask].hist('Planet Mass or Mass*sin(i) [Earth Mass]', bins=100, ax=axes[0], range=[0, 1250])
axes[0].set_title("Exoplanètes découvertes par TESS")

rect = ptch.Rectangle((0, 0.5), 300, 30, fill=False, color="red", linewidth=2)
axes[0].add_patch(rect)

mask = tcp["Planet Mass or Mass*sin(i) [Earth Mass]"] > 0
tcp[mask].hist('Planet Mass or Mass*sin(i) [Earth Mass]', bins=100, ax=axes[1], range=[0, 300])
axes[1].set_title("Exoplanètes découvertes par TESS\n(zoom)")

plt.suptitle("Répartition des masses des planètes\n[Unité de masse de la Terre]", y=1.05);
# -

# On remarque que la très grande majorité des exoplanètes découvertes ont une masse du __même ordre de grandeur__ que celle de la Terre.

# ***

# #### Répartition des températures d'équilibre

# +
fig, axes = plt.subplots(2, 2, figsize=(10, 10))

# Ici pour les exoplanètes découvertes par TESS
tcp.hist('Equilibrium Temperature [K]', bins=100, ax=axes[0, 0], range=[0, 3000]);
axes[0, 0].set_title("Exoplanètes découvertes par TESS")

# Ici pour les exoplanètes éventuelles découvertes par TESS
tp['Planet Equilibrium Temperature Value [K]'].hist(bins=100, ax=axes[0, 1], range=[0, 3000])
axes[0, 1].set_title("Exoplanètes éventuelles découvertes par TESS")

# Ici pour les exoplanètes potentielles et effectivement découvertes par K2
k2['Equilibrium Temperature [K]'].hist(bins=100, ax=axes[1, 0], range=[0, 3000]);
axes[1, 0].set_title("Exoplanètes potentielles et effectivement\n découvertes par K2")

# Ici pour l'ensemble des exoplanètes confirmées
df_Teq.hist(bins=100, ax=axes[1,1], range=[0, 3000]);
axes[1, 1].set_title("Ensemble des exoplanètes confirmées")

fig.suptitle("Répartition des températures d'équilibre [K]", y=0.95);
# -

# # TODO : commentaires

# ***

# #### Corrélation entre le température d'une planète et son insolation

# +
fig = plt.figure(figsize=(16, 8))
fig.suptitle("Corrélation entre température et insolation [K]")
subfigs = fig.subfigures(1, 2)

axes = subfigs[0].subplots(2, 2)

# Ici pour les exoplanètes découvertes par TESS
tcp.plot.scatter(x='Insolation Flux [Earth Flux]', y='Equilibrium Temperature [K]', color='b', ax=axes[0][0]);
axes[0][0].set_title("Exoplanètes découvertes par TESS");

# Ici pour les exoplanètes éventuelles découvertes par TESS
tp.plot.scatter(x='Planet Insolation Value [Earth flux]', y='Planet Equilibrium Temperature Value [K]', color='g', ax=axes[0][1])
axes[0][1].set_title("Exoplanètes éventuelles découvertes par TESS");

# Ici pour les exoplanètes potentielles et effectivement découvertes par K2
k2.plot.scatter(x='Insolation Flux [Earth Flux]', y='Equilibrium Temperature [K]', color='orange', ax=axes[1][0])
axes[1][0].set_title("Exoplanètes potentielles et effectivement\n découvertes par K2");

# Ici pour l'ensemble des exoplanètes confirmées
df_ti.plot.scatter(x='Insolation Flux [Earth Flux]', y='Equilibrium Temperature [K]', color='r', ax=axes[1][1])
axes[1][1].set_title("Ensemble des exoplanètes confirmées");

# Toutes sur un même graphe
ax2 = subfigs[1].subplots(1, 1)

tcp.plot.scatter(x='Insolation Flux [Earth Flux]', y='Equilibrium Temperature [K]', color='b', ax=ax2)
tp.plot.scatter(x='Planet Insolation Value [Earth flux]', y='Planet Equilibrium Temperature Value [K]', color='g', ax=ax2)
k2.plot.scatter(x='Insolation Flux [Earth Flux]', y='Equilibrium Temperature [K]', color='orange', ax=ax2)
df_ti.plot.scatter(x='Insolation Flux [Earth Flux]', y='Equilibrium Temperature [K]', color='r', ax=ax2)

fig.tight_layout()
ax2.set_title("Ensemble des données");
# -

#

# ***

# #### Corrélation entre la température d'une planète et la température de son étoile

# Ici pour l'ensemble des exoplanètes confirmées
tcp.plot.scatter(y='Equilibrium Temperature [K]', x='Stellar Effective Temperature [K]');

# Ici pour les exoplanètes éventuelles découvertes par TESS
tp.plot.scatter(x = 'Stellar Effective Temperature Value [K]', y = 'Planet Equilibrium Temperature Value [K]');

# Ici pour les exoplanètes potentielles et effectivement découvertes par K2
k2.plot.scatter(x='Insolation Flux [Earth Flux]',y='Equilibrium Temperature [K]');

# ***

# #### Corrélation entre la période de rotation d'une planète et son rayon

# Ici pour l'ensemble des exoplanètes confirmées
tcp.plot.scatter(y='Orbital Period [days]', x='Planet Radius [Earth Radius]');

# Ici pour les exoplanètes éventuelles découvertes par TESS
tp.plot.scatter(x = 'Planet Orbital Period Value [days]', y = 'Planet Radius Value [R_Earth]');

# Ici pour les exoplanètes potentielles et effectivement découvertes par K2
k2.plot.scatter(y='Planet Radius [Earth Radius]',x='Orbital Period [days]');

# ***

# #### Corrélation entre le rayon d'une planète et sa température d'équilibre

# Ici pour l'ensemble des exoplanètes confirmées
tcp.plot.scatter(x='Equilibrium Temperature [K]', y='Planet Radius [Earth Radius]');

# Ici pour les exoplanètes potentielles et effectivement découvertes par K2
k2.plot.scatter(y='Planet Radius [Earth Radius]',x='Equilibrium Temperature [K]');

# ***

# #### Lien entre le rayon d'une planète et sa température d'équilibre en fonction de l'année

# On retire les warnings disgracieux provoqués par seaborn
import warnings
warnings.filterwarnings('ignore')

# Ici pour l'ensemble des exoplanètes confirmées
sns.relplot(data=tcp, x='Distance [pc]', y='Stellar Radius [Solar Radius]', hue='Discovery Year');

# ***

# #### Lien entre la température d'une planètes et de son étoile en fonction de l'insolation de l'étoile

# Ici pour l'ensemble des exoplanètes confirmées
sns.relplot(data=tcp, x='Stellar Effective Temperature [K]', hue='Insolation Flux [Earth Flux]', y='Equilibrium Temperature [K]');

# ***

# #### Efficacité des méthodes de découverte d'exoplanètes

# Ici pour l'ensemble des exoplanètes confirmées
explode = [0.8, 0, 0.4, 0.8, 0, 0.2, 0.5, 0.3, 0,0,0.2]
df_eff.groupby(by='Discovery Method').count().plot(y='Planet Name', kind='pie', figsize=(15, 15), autopct='%0.2f%%', explode=explode)
plt.title('Moyens de découverte les plus efficaces');

df_eff.pivot_table(index='Discovery Method', aggfunc='count').head()

# On voit donc que la technique dite du Transit est largement majoritaire

# ***

# #### Évolution de notre distance aux planètes découvertes en fonction du temps

df_disc[["Discovery_Year", "Distance [pc]"]].groupby(by="Discovery_Year").mean().plot()
plt.title("Distance moyenne entre la terre et les planètes découvertes dans l'année (en pc)");

# A part quelques valeurs particulières en 1992, on voit que l'on découvre des planètes de plus en plus lointaines
