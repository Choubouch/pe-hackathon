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
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
#   language_info:
#     name: python
#     nbconvert_exporter: python
#     pygments_lexer: ipython3
# ---

# %% [markdown]
# # tess_projects
#
# sauvé en Python

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import utility as util

# %% [markdown]
# On commence par importer les données. Ici ce sont les planètes qui ont été identifiées par le telescope TESS comme étant d'éventuelles exoplanètes, mais non prouvé
# Ensuite on selectionne les colonnes avec des données pertinentes, et qui sont communes aux autres tables pour pouvoir comparer. L'idée est de pouvoir faire des tracés communs avec les tables qui continnent les exoplanètes prouvées pour voire si les exoplanètes éventuelles sont pertinentes

# %%
tp = pd.read_csv('tess_project_candidates.csv', skiprows = 69)

assoc = util.get_rename_assoc('tess_project_candidates.csv')
tp.rename(columns=assoc, inplace=True)
tp = tp[['TESS Object of Interest','TESS Input Catalog ID','RA [sexagesimal]','Dec [sexagesimal]','Planet Orbital Period Value [days]','Planet Radius Value [R_Earth]','Planet Insolation Value [Earth flux]','Planet Equilibrium Temperature Value [K]','Stellar Distance [pc]','Stellar Effective Temperature Value [K]','Stellar Radius Value [R_Sun]']]
tp.set_index('TESS Object of Interest', inplace = True)
tp.head()

# %%
tp.shape

# %% [markdown]
# On enlève les lignes où il y a des valeurs NaN

# %%
tp.dropna(how = 'any', inplace = True)
tp.shape

# %%
tp.head()

# %% [markdown]
# ### On commence par regarder grossièrement les données (notamment les moyennes)

# %%
tp.describe()

# %% [markdown]
# ### On trace la répartition des températures d'équilibre des planètes

# %%
tp['Planet Equilibrium Temperature Value [K]'].hist(bins = 100, legend = True)

# %% [markdown]
# ### Ici on test la répartition des rayons des planètes

# %%
tp['Planet Radius Value [R_Earth]'].hist(bins = 100, legend = True)

# %% [markdown]
# On voit qu'il y a des valeurs très élevée qui dégradent l'affichage, on froce donc la fenetre

# %%
tp['Planet Radius Value [R_Earth]'].hist(bins = 100, legend = True, range = [0,50])

# %% [markdown]
# ### Là on regarde le lien qui existe entre la temperature de la planète et la temperature de son étoile

# %%
tp.plot.scatter(x = 'Stellar Effective Temperature Value [K]', y = 'Planet Equilibrium Temperature Value [K]')

# %% [markdown]
# ### Et là entre la période de révolution et le rayon de l'étoile

# %%
tp.plot.scatter(y = 'Stellar Radius Value [R_Sun]', x = 'Planet Orbital Period Value [days]')

# %% [markdown]
# On voit on tracé un peu bizarre

# %% [markdown]
# ### On regarde alors le rayon de la planète en fonction de la periode

# %%
tp.plot.scatter(x = 'Planet Orbital Period Value [days]', y = 'Planet Radius Value [R_Earth]')

# %% [markdown]
# ### Là on regarde la corrélation entre la temperature de la planète et l'insolation qu'elle reçoit

# %%
tp.plot.scatter(x = 'Planet Insolation Value [Earth flux]', y = 'Planet Equilibrium Temperature Value [K]')

# %% [markdown]
# On voit une jolie loi qui semble se dessiner

# %% [markdown]
# ### On va regarder le lien entre rayon de la planète et temperature d'équilibre

# %%
tp.plot.scatter(x = 'Planet Equilibrium Temperature Value [K]', y = 'Planet Radius Value [R_Earth]')
