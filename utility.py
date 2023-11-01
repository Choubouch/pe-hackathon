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
# # Utilitaires

# %% [markdown]
# ## `get_rename_assoc`
# ### Input
# file (str) - Le chemin vers un fichier CSV
# ### Output
# (dict) - Un dictionnaire qui associe à chaque nom de colonne du CSV un nom plus explicite (à retravailler)
# ### Usage
# ```py
# import pandas as pd
# import utility as util
# df = pd.read_csv(file)
#
# assoc = util.get_rename_assoc(file)
# df.rename(columns=assoc, inplace=True)
# ```

# %%
def get_rename_assoc(file):
    with open(file, 'r') as f:
        assoc = {}
    
        for ligne in f:
            l = ligne.strip().split(' ')
            
            if len(l) > 1 and l[1] == "COLUMN":
                nom_col = l[2]
                assoc[ nom_col[:-1] ] = ' '.join(l[3:]).strip()
    return assoc

# %% [markdown]
# ***
