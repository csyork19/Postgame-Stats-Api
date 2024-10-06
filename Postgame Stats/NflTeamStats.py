import pandas as pd
import nfl_datq_py as nfl
import matplotlib.pyplot as plt
from matplotlib import style

# Display maximum columns
pd.set_option('display.max_columns', None)


df = nfl.import_ngs_data(stat_type='passing')
year = 2022

# Filter down to week = 0, full season data for the year(s) specified
df = df[df['week'] == 0]
df = df[df['season'] == year]
df = df.reset_index()
print(df)

# Calculate the average time to throw and completion % above expectation
average_ttt = df['avg_time_to_throw'].mean()
average_cpae = df['completion_percentage_above_expectation'].mean()

average_cpae