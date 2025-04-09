import pandas as pd
import numpy as np
import streamlit as st


@st.cache_data
def load_data():
    return(pd.read_csv("./ShotData/get_game_shot_data_multiple_seasons2022_2024.csv"))


@st.cache_data
def extract_lineup(df):
    # Calcule le temps de jeu d un line up
    df["MARKERTIME"]=df.apply(lambda row: "10:00" if row["PLAYINFO"]=="Begin Period" else row["MARKERTIME"],axis=1)
    df["MARKERTIME"]=df.apply(lambda row: "00:00" if row["PLAYINFO"] in ["End Period","End Game"] else row["MARKERTIME"],axis=1)
    df["lineup"]=df["Lineup_A"].apply(lambda x: "_".join(sorted(eval(x))))
    df["FGA"]=df["PLAYTYPE"].apply(lambda x: 1 if "FGA" in x else 0)
    df["FGM"]=df["PLAYTYPE"].apply(lambda x: 1 if "FGM" in x else 0)
    df["O"]=df["PLAYTYPE"].apply(lambda x: 1 if x=="O" else 0)
    df["FTA"]=df["PLAYTYPE"].apply(lambda x: 1 if x=="FTA" else 0)
    df["TO"]=df["PLAYTYPE"].apply(lambda x: 1 if x=="TO" else 0)
    df["D"]=df["PLAYTYPE"].apply(lambda x: 1 if x=="D" else 0)
    df.IsHomeTeam=df.IsHomeTeam.fillna(False)

    data_home=df[["Gamecode","MARKERTIME","PERIOD","lineup","FGA","FGM","O","TO","D","FTA","IsHomeTeam"]]
    for i in ["FGA","FTA","FGM","O","TO","D"]:
        data_home[i]=data_home[i]*data_home.IsHomeTeam.astype(int).fillna(0)
    
    #st.write(data_home)

    df["lineup"]=df["Lineup_B"].apply(lambda x: "_".join(sorted(eval(x))))
    data_vis=df[["Gamecode","MARKERTIME","PERIOD","lineup","FGA","FGM","O","TO","D","FTA","IsHomeTeam"]]
    data_vis.IsHomeTeam=abs(data_vis.IsHomeTeam-1)
    for i in ["FGA","FTA","FGM","O","TO","D"]:
        data_vis[i]=data_vis[i]*data_vis.IsHomeTeam.astype(int).fillna(0)
    
    data=pd.concat([data_home,data_vis])

    data=data[data.MARKERTIME==data.MARKERTIME]
    data["number"]=range(1,len(data)+1)
    
    data["lineup_n"] = (df['lineup'] != df['lineup'].shift()).cumsum()
    data["time"]=data.MARKERTIME.apply(lambda x: int(x.split(":")[0])*60+int(x.split(":")[1]))
    data=data.groupby(["Gamecode","PERIOD",'lineup_n']).agg({"lineup":"first", 
                         'time': lambda x: x.max() - x.min(),
                         "FGA":"sum",
                         "FGM":"sum",
                         "O":"sum",
                         "D":"sum",
                         "TO":"sum",
                         "FTA":"sum"
                         })
    data=data[data.time>0]
    data=data.groupby("lineup", as_index=False).agg({"lineup":"first", 
                         'time': "sum",
                         "FGA":"sum",
                         "FGM":"sum",
                         "O":"sum",
                         "D":"sum",
                         "TO":"sum",
                         "FTA":"sum"
                        })
    data["Poss1"]=data["FGA"]+0.44*data["FTA"]-data["O"]+data["TO"]
    data["Poss2"]=data["FGA"]+0.44*data["FTA"]-1.07*data["O"]/(data["O"]+data["D"])*(data["FGA"]-data["FGM"])+data["TO"]

    return(data)
