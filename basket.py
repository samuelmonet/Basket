import streamlit as st 
import pandas as pd
import numpy as np
from streamlit_option_menu import option_menu # for sidebar
from euroleague_api.shot_data import ShotData
from euroleague_api.play_by_play_data import PlayByPlay
import plotly.graph_objects as go

st.set_page_config(layout="wide")

def main():	
	
	with st.sidebar:		
		st.title('Un titre') # Write as a title (bigger) other displays are header, write, caption
		season=st.selectbox(":red[1. Select the season]", [2022,2023,2024])
		game_code=st.selectbox(":red[1. Select the game code]", range(1,20)) 
		competition_code=st.selectbox(":red[2. Select the competition code]",["E","U"])
		shotdata = ShotData(competition_code)
		df = shotdata.get_game_shot_data(season, game_code)
		playdata = PlayByPlay(competition_code)
		players = playdata.get_game_play_by_play_data(season, game_code)

		
	st.write(df)
	st.write(players)
	st.subheader("Positions des tirs")
	shots=df[df.ID_ACTION.isin(["2FGA", "2FGM", "3FGA", "3FGM"])][["PLAYER","POINTS","COORD_X","COORD_Y"]]
	shots["point"] = shots.POINTS.apply(lambda x: 1 if x>0 else 0)
	player=st.selectbox("Selectionner un joueur",["All"]+df.PLAYER.unique().tolist())
	if player!="All":
		shots=shots[shots.PLAYER==player]
	c1,c2=st.columns([2,1])
	fig = go.Figure()
	fig.add_trace(go.Scatter(
            x=shots[shots.point==1]["COORD_X"], y=shots[shots.point==1]["COORD_Y"],
            name='Scored',
            mode='markers',
            marker_color='rgba(0, 152, 0, 1)'
            ))
	fig.add_trace(go.Scatter(
            x=shots[shots.point==0]["COORD_X"], y=shots[shots.point==1]["COORD_Y"],
            name='Missed',
            mode='markers',
            marker_color='rgba(152, 0, 0, 1)'
            ))
	fig.update_traces(mode='markers', marker_line_width=2, marker_size=10)
	fig.update_layout(title=dict(text='Titre du plot'),
                  yaxis_zeroline=False, xaxis_zeroline=False)
	c1.plotly_chart(fig, use_container_width=True)
	c2.write(shots)

   
	
	








if __name__ == '__main__':
	main()
