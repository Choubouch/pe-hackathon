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
# ## Etape 1 : nettoyage de la table de données
#
# Cette étape consiste à rendre la table confirmed_planet.csv propre à l'exploitation

# %%
import pandas as pd
import utility as util
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

# %%
df_brut = pd.read_csv("confirmed_planets.csv", skiprows = 96)
assoc = util.get_rename_assoc("confirmed_planets.csv")
df_brut.rename(columns=assoc, inplace=True)

# %%
df_brut.head()

# %%
df = df_brut.drop(['Date of Last Update', 'Controversial Flag', 'Spectral Type', 'Stellar Parameter Reference',
                  'Stellar Metallicity [dex]', 'Stellar Metallicity Upper Unc. [dex]', 'Stellar Metallicity Lower Unc. [dex]',
                  'Stellar Metallicity Limit Flag', 'Stellar Metallicity Ratio', 'Release Date'], axis = 1)

# %% [markdown]
# On commence pas supprimer les colonnes dont on sait qu'on ne se servira pas (par exemples les colonnes dont je ne comprends pas trop l'utilité)

# %%
df_brut.columns

# %%
df.head()

# %%
df.info()

# %% [markdown]
# ## Etape 2 : étude statistique de la base 

# %% [markdown]
# ### a - Les découvertes d'exoplanetes dans le temps

# %%
df_disc = df[['Planet Name', 'Host Name', 'Number of Planets', 'Discovery Method', 'Discovery Year', 'Discovery Facility', 'Planet Radius [Earth Radius]', 'Distance [pc]'  ]]

# %%
df_disc.rename(columns={'Discovery Year' : 'Discovery_Year'}, inplace=True)
df_disc.head(10)

# %%

# %%
X = np.sort(df_disc["Discovery_Year"].unique())

# %%
Y = []

# %%
for i in X : 
    tab = df_disc.query(f'Discovery_Year == {i}')
    a = len(tab['Planet Name'].unique())
    Y.append(a)

# %%
a = 2007
df_disc.query(f'Discovery_Year == {a}').head()

# %%
Y

# %%
plt.bar(X,Y)
plt.title('Découvertes de planètes en fonction du temps')

# %%
Y2 = []
for i in X : 
    tab = df_disc.query(f'Discovery_Year == {i}')
    group_name = tab.groupby(by = 'Planet Name')
    a = group_name['Distance [pc]'].mean().mean()
    Y2.append(a)

# %%
plt.plot(X, Y2)
plt.title('Distance moyenne entre la terre et les planètes découvertes dans l année (en pc)')

# %% [markdown]
# A part quelques valeurs particulières en 1992, on voit que l'on découvre des planètes de plus en plus lointaines

# %% [markdown]
# ### b - Température d'équilibre et insolation

# %%
df_ti = df[['Planet Name','Equilibrium Temperature [K]', 'Insolation Flux [Earth Flux]']]

# %%
df_ti.head()

# %%
df_ti = df_ti.drop_duplicates()

# %% [markdown]
# Je viens de découvir cette commande qui permet d'enlever les lignes en double et qui m'aurait été bien utile précédemment

# %%
df_ti = df_ti.dropna()
df_ti.shape

# %%
df_ti.plot.scatter(x='Insolation Flux [Earth Flux]', y='Equilibrium Temperature [K]')

# %% [markdown]
# ### c - Méthodes de découvertes les plus efficaces

# %%
df_eff = df[['Planet Name', 'Discovery Method']]

# %%
df_eff.head()

# %%
df_eff = df_eff.drop_duplicates()

# %%
df_eff.head(10)

# %%
group = df_eff.groupby(by = 'Discovery Method')

# %%
explode = [0.8, 0, 0.4, 0.8, 0, 0.2, 0.5, 0.3, 0,0,0.2]
group.count().plot(y='Planet Name', kind='pie', figsize=(15, 15), autopct='%0.2f%%', explode = explode)
plt.title('Moyens de découverte les plus efficaces')

# %% [markdown]
# ### d - répartition T eq

# %%
df_Teq = df[['Planet Name', 'Equilibrium Temperature [K]']]

# %%
df_Teq = df_Teq.drop_duplicates()
df_Teq = df_Teq.dropna()

# %%
df_Teq.hist(bins = 100)

# %%
