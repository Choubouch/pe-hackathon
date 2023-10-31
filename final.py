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

# ## Traitement des données

tcp.hist('Discovery Year', bins=50);

tcp.hist('Planet Radius [Earth Radius]', bins=50);

tcp.hist('Planet Mass or Mass*sin(i) [Earth Mass]', bins=50);

tcp.hist('Equilibrium Temperature [K]', bins=50);

tcp.plot.scatter(y='Equilibrium Temperature [K]', x='Insolation Flux [Earth Flux]');

tcp.plot.scatter(y='Equilibrium Temperature [K]', x='Stellar Effective Temperature [K]');

tcp.plot.scatter(y='Orbital Period [days]', x='Planet Radius [Earth Radius]');

tcp.plot.scatter(x='Equilibrium Temperature [K]', y='Planet Radius [Earth Radius]');

sns.relplot(data=tcp, x='Distance [pc]', y='Stellar Radius [Solar Radius]', hue='Discovery Year');

sns.relplot(data=tcp, x='Stellar Effective Temperature [K]', hue='Insolation Flux [Earth Flux]', y='Equilibrium Temperature [K]');

sns.relplot(data=tcp, x='Stellar Effective Temperature [K]', hue='Insolation Flux [Earth Flux]', y='Equilibrium Temperature [K]');


