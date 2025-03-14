import streamlit as st 
import pandas as pd
import numpy as np
from streamlit_option_menu import option_menu # for sidebar
from euroleague_api.shot_data import ShotData
from euroleague_api.play_by_play_data import PlayByPlay
from scipy.stats import norm, gaussian_kde, percentileofscore
import plotly.graph_objects as go

# import fonctions.py as f

def main():	
	
	with st.sidebar:		
		st.title('Un titre') # Write as a title (bigger) other displays are header, write, caption
		season=st.selectbox(":red[1. Select the season]", [2022,2023,2024])
		game_code=st.selectbox(":red[1. Select the game code]", range(1,100)) 
		competition_code=st.selectbox(":red[2. Select the competition code]",["E","U"])
		shotdata = ShotData(competition_code)
		df = shotdata.get_game_shot_data(season, game_code)  
		playdata = PlayByPlay(competition_code)
		players = playdata.get_pbp_data_with_lineups_single_season(season)
        	
	st.write(df)
	st.write(players)

if __name__ == '__main__':
	main()
