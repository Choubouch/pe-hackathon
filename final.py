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

# Nous avons trouvé 4 bases de données à exploiter, elles contiennent les exoplanètes ou les candidats à être des exoplanètes. Deux proviennent du satellite TESS et une du satellite K2 et la dernière regroupe l'ensemble des exoplanètes confirmées

# ## Nettoyage des bases de données

# Pour les exoplanètes trouvées par TESS

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

Pour le satellite K2

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

# Pour l'ensemble des exoplanètes

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

# Ici pour les exoplanètes trouvées par TESS
tcp.hist('Discovery Year', bins=50);

# Ici pour les exoplanètes potentielles et effectivement trouvées par K2
k2.hist('Discovery Year')

#découverte d'exoplanètes confirmées
X = np.sort(df_disc["Discovery_Year"].unique())

# +
Y = []
for i in X :  #J'ai fait un for car à ce moment je n'avais pas encore trouvé la commande drop_duplicates pour 
              #retirer les planètes qui apparaissaient en triple (chaque planète a 3 lignes identiques dans le dataframe)
    tab = df_disc.query(f'Discovery_Year == {i}')
    a = len(tab['Planet Name'].unique())
    Y.append(a)

plt.bar(X,Y)
plt.title('Découvertes de planètes en fonction du temps')
# -

# On voit que les découvertes d'exoplanètes augementent dans le temps, ce qui est cohérent avec les fait que les téléscopes sont de plus en plus perfectionnés.

#

# #### Répartition des rayons des planètes

# Ici pour les exoplanètes trouvées par TESS
tcp.hist('Planet Radius [Earth Radius]', bins=50);

# Ici pour les exoplanètes éventuelles trouvées par TESS
tp['Planet Radius Value [R_Earth]'].hist(bins = 100, legend = True)

# Ici pour les exoplanètes potentielles et effectivement trouvées par K2
k2['Planet Radius [Earth Radius]'].hist(bins=100, legend = True)

# #### Répartition des masses des planètes

# Ici pour les exoplanètes trouvées par TESS
tcp.hist('Planet Mass or Mass*sin(i) [Earth Mass]', bins=50);

# #### Répartition des températures d'équilibre

# Ici pour les exoplanètes trouvées par TESS
tcp.hist('Equilibrium Temperature [K]', bins=50);

# Ici pour les exoplanètes éventuelles trouvées par TESS
tp['Planet Equilibrium Temperature Value [K]'].hist(bins = 100, legend = True)

# Ici pour les exoplanètes potentielles et effectivement trouvées par K2
k2['Equilibrium Temperature [K]'].hist(bins=500, legend = True)

#température d'équilibre des exoplanètes confirmées
df_Teq.hist(bins = 100)

# #### Corrélation entre température de la planète et insolation

# Ici pour les exoplanètes trouvées par TESS
tcp.plot.scatter(y='Equilibrium Temperature [K]', x='Insolation Flux [Earth Flux]');

# Ici pour les exoplanètes éventuelles trouvées par TESS
tp.plot.scatter(x = 'Planet Insolation Value [Earth flux]', y = 'Planet Equilibrium Temperature Value [K]')

# Ici pour les exoplanètes potentielles et effectivement trouvées par K2
k2.plot.scatter(x='Insolation Flux [Earth Flux]',y='Equilibrium Temperature [K]')

#Pour les exoplanètes confirmées
df_ti.plot.scatter(x='Insolation Flux [Earth Flux]', y='Equilibrium Temperature [K]')

# #### Corrélation entre température de la planète et température de son étoile

#Pour les exoplanètes confirmées
tcp.plot.scatter(y='Equilibrium Temperature [K]', x='Stellar Effective Temperature [K]');

# Ici pour les exoplanètes éventuelles trouvées par TESS
tp.plot.scatter(x = 'Stellar Effective Temperature Value [K]', y = 'Planet Equilibrium Temperature Value [K]')

# Ici pour les exoplanètes potentielles et effectivement trouvées par K2
k2.plot.scatter(x='Insolation Flux [Earth Flux]',y='Equilibrium Temperature [K]')

# #### Corrélation entre période de rotation et rayon de la planète

#Pour les exoplanètes confirmées
tcp.plot.scatter(y='Orbital Period [days]', x='Planet Radius [Earth Radius]');

# Ici pour les exoplanètes éventuelles trouvées par TESS
tp.plot.scatter(x = 'Planet Orbital Period Value [days]', y = 'Planet Radius Value [R_Earth]')

# Ici pour les exoplanètes potentielles et effectivement trouvées par K2
k2.plot.scatter(y='Planet Radius [Earth Radius]',x='Orbital Period [days]')

# #### Corrélation du rayon des planètes en fonction de la température d'équilibre

#Pour les exoplanètes confirmées
tcp.plot.scatter(x='Equilibrium Temperature [K]', y='Planet Radius [Earth Radius]');

# Ici pour les exoplanètes potentielles et effectivement trouvées par K2
k2.plot.scatter(y='Planet Radius [Earth Radius]',x='Equilibrium Temperature [K]')

# #### Lien entre rayon des planètes et température d'équilibre en fonction de l'année

#Pour les exoplanètes confirmées
sns.relplot(data=tcp, x='Distance [pc]', y='Stellar Radius [Solar Radius]', hue='Discovery Year');

# #### Lien entre température des planètes et de leur étoile en fonction de l'insolation des étoiles

#Pour les exoplanètes confirmées
sns.relplot(data=tcp, x='Stellar Effective Temperature [K]', hue='Insolation Flux [Earth Flux]', y='Equilibrium Temperature [K]');

# #### Les méthodes de découvertes d'exoplanètes les plus efficaces

#pour les exoplanètes confirmées, les techniques qui donnent le plus de résultats
explode = [0.8, 0, 0.4, 0.8, 0, 0.2, 0.5, 0.3, 0,0,0.2]
group.count().plot(y='Planet Name', kind='pie', figsize=(15, 15), autopct='%0.2f%%', explode = explode)
plt.title('Moyens de découverte les plus efficaces')

# On voit donc que la technique dite du Transit est largement majoritaire

# #### Distance des planètes découvertes en fonction du temps

Y2 = []
for i in X : 
    tab = df_disc.query(f'Discovery_Year == {i}')
    group_name = tab.groupby(by = 'Planet Name')
    a = group_name['Distance [pc]'].mean().mean()
    Y2.append(a)
plt.plot(X, Y2)
plt.title('Distance moyenne entre la terre et les planètes découvertes dans l année (en pc)')

# A part quelques valeurs particulières en 1992, on voit que l'on découvre des planètes de plus en plus lointaines




















