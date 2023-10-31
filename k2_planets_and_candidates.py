import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('k2_planets_and_candidates.csv', skiprows = 98)
df.head()

df.describe()


