import streamlit as st 
import pandas as pd
import numpy as np
import requests
from streamlit_option_menu import option_menu # for sidebar
from euroleague_api.shot_data import ShotData
from euroleague_api.play_by_play_data import PlayByPlay
from scipy.stats import norm, gaussian_kde, percentileofscore
import plotly.graph_objects as go

import matplotlib.pyplot as plt
import seaborn as sns

from matplotlib import cm
from matplotlib.patches import Circle, Rectangle, Arc, ConnectionPatch
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.colors import LinearSegmentedColormap, ListedColormap, BoundaryNorm
from matplotlib.path import Path
from matplotlib.patches import PathPatch

import requests
import pandas as pd
from shot_chart_plots import plot_scatter, joint_plot


url = "https://live.euroleague.net/api/Points?gamecode=54&seasoncode=E2021"

r = requests.get(url)
print(r.status_code)  # if all goes well this must return 200

data = r.json()
shots_df = pd.DataFrame(data['Rows'])
shots_df['TEAM'] = shots_df['TEAM'].str.strip()  # team id contains trailing white space
shots_df['ID_PLAYER'] = shots_df['ID_PLAYER'].str.strip()  # player id contains trailing white space

# split the home and away teams, their made and missed shots
home_df = shots_df[shots_df['TEAM'] == 'PAN']
fg_made_home_df = home_df[home_df['ID_ACTION'].isin(['2FGM', '3FGM'])]
fg_miss_home_df = home_df[home_df['ID_ACTION'].isin(['2FGA', '3FGA'])]

away_df = shots_df[shots_df['TEAM'] == 'IST']
fg_made_away_df = away_df[away_df['ID_ACTION'].isin(['2FGM', '3FGM'])]
fg_miss_away_df = away_df[away_df['ID_ACTION'].isin(['2FGA', '3FGA'])]

# scatter shot chart of PAOs
plot_scatter(fg_made_home_df, fg_miss_home_df, title='PAO')

# scatter shot chart of Efer
plot_scatter(fg_made_away_df, fg_miss_away_df, title='EFES')

# density plot of all PAO's shots (made and missed)
fg_home_shots = pd.concat((fg_made_home_df, fg_miss_home_df), axis=0)
joint_plot(fg_home_shots, title='PAOs Attemped Shots (made and missed)')