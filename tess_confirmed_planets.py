# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: all,-hidden,-heading_collapsed,-run_control,-trusted
#     notebook_metadata_filter: all, -jupytext.text_representation.jupytext_version,
#       -jupytext.text_representation.format_version,-language_info.version, -language_info.codemirror_mode.version,
#       -language_info.codemirror_mode,-language_info.file_extension, -language_info.mimetype,
#       -toc, -rise, -version
#     text_representation:
#       extension: .py
#       format_name: percent
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
#   language_info:
#     name: python
#     nbconvert_exporter: python
#     pygments_lexer: ipython3
# ---

# %% [markdown]
# # Nettoyage de TESS Confirmed Planets

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import utility as util

# %%
df = pd.read_csv('tess_confirmed_planet.csv', skiprows=99)
df.head()

# %%
assoc = util.get_rename_assoc('tess_confirmed_planet.csv')
df.rename(columns=assoc, inplace=True)
df.head()

# %%
# On regarde le nombre d'enregistrements dans la base de données
df.shape[0]

# %%
# On vérifie que la première colonne peut constituer un index
len(df['Planet Name'].unique())

# %%
df.set_index('Planet Name', inplace=True)
df.head()

# %%
to_drop = ['Planetary Parameter Reference', 'Stellar Parameter Reference', 'Default Parameter Set', 'Controversial Flag', 'Stellar Metallicity Ratio']

df.drop(to_drop, axis=1, inplace=True)
df.head()

# %%
df.columns

# %%
planet_discovery = df[['Host Name', 'Number of Stars', 'Number of Planets', 'Discovery Method', 'Discovery Year', 'Discovery Facility', 'Solution Type',
        'Distance [pc]', 'Date of Last Update',
       'Planetary Parameter Reference Publication Date', 'Release Date']]
planet_orbit = df[['Orbital Period [days]', 'Orbital Period Upper Unc. [days]', 'Orbital Period Lower Unc. [days]', 'Orbital Period Limit Flag',
'Orbit Semi-Major Axis [au])', 'Orbit Semi-Major Axis Upper Unc. [au]', 'Orbit Semi-Major Axis Lower Unc. [au]', 'Orbit Semi-Major Axis Limit Flag']]
planet_radius = df[['Planet Radius [Earth Radius]', 'Planet Radius Upper Unc. [Earth Radius]', 'Planet Radius Lower Unc. [Earth Radius]',
       'Planet Radius [Jupiter Radius]',
       'Planet Radius Upper Unc. [Jupiter Radius]',
       'Planet Radius Lower Unc. [Jupiter Radius]', 'Planet Radius Limit Flag']]
planet_mass = df[['Planet Mass or Mass*sin(i) [Earth Mass]',
       'Planet Mass or Mass*sin(i) [Earth Mass] Upper Unc.',
       'Planet Mass or Mass*sin(i) [Earth Mass] Lower Unc.',
       'Planet Mass or Mass*sin(i) [Earth Mass] Limit Flag',
       'Planet Mass or Mass*sin(i) [Jupiter Mass]',
       'Planet Mass or Mass*sin(i) [Jupiter Mass] Upper Unc.',
       'Planet Mass or Mass*sin(i) [Jupiter Mass] Lower Unc.',
       'Planet Mass or Mass*sin(i) [Jupiter Mass] Limit Flag',
       'Planet Mass or Mass*sin(i) Provenance']]
planet_excentricity = df[['Eccentricity',
       'Eccentricity Upper Unc.', 'Eccentricity Lower Unc.',
       'Eccentricity Limit Flag']]
planet_insolation = df[['Insolation Flux [Earth Flux]',
       'Insolation Flux Upper Unc. [Earth Flux]',
       'Insolation Flux Lower Unc. [Earth Flux]', 'Insolation Flux Limit Flag',
       'Equilibrium Temperature [K]', 'Equilibrium Temperature Upper Unc. [K]',
       'Equilibrium Temperature Lower Unc. [K]',
       'Equilibrium Temperature Limit Flag']]
planet_stellar = df[['Stellar Effective Temperature [K]',
       'Stellar Effective Temperature Upper Unc. [K]',
       'Stellar Effective Temperature Lower Unc. [K]',
       'Stellar Effective Temperature Limit Flag',
       'Stellar Radius [Solar Radius]',
       'Stellar Radius Upper Unc. [Solar Radius]',
       'Stellar Radius Lower Unc. [Solar Radius]', 'Stellar Radius Limit Flag',
       'Stellar Mass [Solar mass]', 'Stellar Mass Upper Unc. [Solar mass]',
       'Stellar Mass Lower Unc. [Solar mass]', 'Stellar Mass Limit Flag',
       'Stellar Metallicity [dex]', 'Stellar Metallicity Upper Unc. [dex]',
       'Stellar Metallicity Lower Unc. [dex]',
       'Stellar Metallicity Limit Flag',
       'Stellar Surface Gravity [log10(cm/s**2)]',
       'Stellar Surface Gravity Upper Unc. [log10(cm/s**2)]',
       'Stellar Surface Gravity Lower Unc. [log10(cm/s**2)]',
       'Stellar Surface Gravity Limit Flag']]

# %%
planet_discovery.head()

# %%
# Gestion du format de dates
planet_discovery.iloc[:, -3] = pd.to_datetime(planet_discovery.iloc[:, -3], format="%Y-%m-%d")
planet_discovery.iloc[:, -2] = pd.to_datetime(planet_discovery.iloc[:, -2], format="%Y-%m")
planet_discovery.iloc[:, -1] = pd.to_datetime(planet_discovery.iloc[:, -1], format="%Y-%m-%d")

# %%
planet_discovery.head()

# %% scrolled=true
planet_radius.head()

# %%
planet_discovery.hist('Discovery Year', bins=50);

# %%
planet_radius.hist('Planet Radius [Earth Radius]', bins=50);

# %%
planet_mass.hist('Planet Mass or Mass*sin(i) [Earth Mass]', bins=50);

# %%
planet_insolation.hist('Equilibrium Temperature [K]', bins=50);

# %%
planet_insolation.plot.scatter(y='Equilibrium Temperature [K]', x='Insolation Flux [Earth Flux]');

# %%
df3 = planet_insolation.merge(planet_stellar, left_index=True, right_index=True)
df3.plot.scatter(y='Equilibrium Temperature [K]', x='Stellar Effective Temperature [K]');

# %%
df3 = planet_radius.merge(planet_orbit, left_index=True, right_index=True)
df3.plot.scatter(y='Orbital Period [days]', x='Planet Radius [Earth Radius]');

# %%
df3 = planet_radius.merge(planet_insolation, left_index=True, right_index=True)
df3.plot.scatter(x='Equilibrium Temperature [K]', y='Planet Radius [Earth Radius]');

# %%
sns.relplot(data=df, x='Distance [pc]', y='Stellar Radius [Solar Radius]', hue='Discovery Year');

# %%
sns.relplot(data=df, x='Stellar Effective Temperature [K]', hue='Insolation Flux [Earth Flux]', y='Equilibrium Temperature [K]');

# %%
sns.relplot(data=df, x='Stellar Effective Temperature [K]', hue='Insolation Flux [Earth Flux]', y='Equilibrium Temperature [K]');
