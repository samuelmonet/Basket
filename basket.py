import streamlit as st 
import pandas as pd
import numpy as np
from streamlit_option_menu import option_menu # for sidebar
from euroleague_api.shot_data import ShotData
from euroleague_api.play_by_play_data import PlayByPlay
from euroleague_api.play_by_play_data import BoxScoreData
import plotly.graph_objects as go
from shot_plot import *
from load import *
from euroleague_api.standings import Standings

st.set_page_config(layout="wide")

def main():	
	
	test=True

	if test:
		df = load_data()
		st.subheader("Positions des tirs")
		c1,c2,c3=st.columns([1,1,1])
		season=c1.selectbox(":red[Select the season]", ["all",2022,2023,2024])
		if season != "all":
			df=df[df.Season==season]

		team=c2.selectbox(":red[Select the Team]", ["all"]+[i for i in df.TEAM.unique()])
		if team != "all":
			df=df[df.TEAM==team]

		player=c3.selectbox(":red[Select the Player]", ["all"]+[i for i in df.PLAYER.unique()])
		if player != "all":
			df=df[df.PLAYER==player]
		
		shots=df[df.ID_ACTION.isin(["2FGA", "2FGM", "3FGA", "3FGM"])][["PLAYER","POINTS","COORD_X","COORD_Y"]]
		shots["point"] = shots.POINTS.apply(lambda x: 1 if x>0 else 0)

		type=c1.selectbox("Select type of plot",["Scatter","Hexagonal Heat","Area Heat"])
		c1,c2=st.columns([1,1])
		c1.title("Scored")
		c2.title("Missed")
		if type=="Scatter":
			c1.pyplot(shot_chart_jointplot("COORD_X","COORD_Y",data=shots[shots.point==1]))
			c2.pyplot(shot_chart_jointplot("COORD_X","COORD_Y",data=shots[shots.point==0]))
		elif type=="Hexagonal Heat":
			c1.pyplot(shot_chart_jointgrid("COORD_X","COORD_Y",data=shots[shots.point==1],joint_type="hex",gridsize=50))
			c2.pyplot(shot_chart_jointgrid("COORD_X","COORD_Y",data=shots[shots.point==0],joint_type="hex",gridsize=50))
		else:
			c1.pyplot(shot_chart_jointgrid("COORD_X","COORD_Y",data=shots[shots.point==1],joint_type="kde"))
			c2.pyplot(shot_chart_jointgrid("COORD_X","COORD_Y",data=shots[shots.point==0],joint_type="kde"))

	df=pd.read_csv("./PlayByPlay/get_pbp_data_with_lineups_single_season_2022.csv")

	st.write(df)
	st.write(df.PLAYTYPE.unique())

	st.write(extract_lineup(df))
	


if __name__ == '__main__':
	main()
