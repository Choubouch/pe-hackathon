import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import utility as util
import seaborn as sns

# Nous avons trouvé 4 bases de données à exploiter, elles contiennent les exoplanètes ou les candidats à être des exoplanètes. Trois proviennent du satellite TESS et celui-ci provient du satellite K2 
# On commence par extraire la base de donnée 

dfa = pd.read_csv('k2_planets_and_candidates.csv', skiprows = 98)
dfa.head()

dfa.describe()



assoc = util.get_rename_assoc('k2_planets_and_candidates.csv')
dfa.rename(columns=assoc, inplace=True)

dfa.head()

dfa.columns

dfa.columns

dfa.drop(['Default Parameter Set','Planetary Parameter Reference','System Parameter Reference',
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

dfa.describe()

df1 = dfa.dropna(how='any') 
# je ne garde dans un premier temps que les lignes ayant toutes les colonnes de renseignées
# je fais une copie et non un inplace afin de ne pas perdre la table initiale et pouvoir élargir l'échantillon considéré au besoin

df1.head()



df1.columns







dfa.columns

dfa.hist('Discovery Year') # donne la répartition des années de découvertes les étoiles



df1[['Discovery Year','Distance [pc]']]

dfa['Stellar Effective Temperature [K]'].hist(bins=500, legend = True)

# +
# trouver valeur pathologique puis l'enlever
# -

dfa['Stellar Effective Temperature [K]'].hist(bins=500, legend = True)

dfa['Planet Radius [Earth Radius]'].hist(bins=100, legend = True)

dfa.plot.scatter(x='Stellar Radius [Solar Radius]',y='Orbital Period [days]')

dfa.plot.scatter(x='Stellar Radius [Solar Radius]',y='Insolation Flux [Earth Flux]')

dfa.plot.scatter(x='Insolation Flux [Earth Flux]',y='Equilibrium Temperature [K]')

dfa.plot.scatter(x='Discovery Year',y='Distance [pc]')

df.plot.scatter(x='Equilibrium Temperature [K]',y='Stellar Effective Temperature [K]')

df.plot.scatter(x='Planet Radius [Earth Radius]',y='Equilibrium Temperature [K]')

df.plot.scatter(x='Planet Radius [Earth Radius]',y='Orbital Period [days]')


























