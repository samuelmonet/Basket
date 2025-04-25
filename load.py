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
    df["3FGM"]=df["PLAYTYPE"].apply(lambda x: 1 if x=="3FGM" else 0)
    df["2FGM"]=df["PLAYTYPE"].apply(lambda x: 1 if x=="2FGM" else 0)
    df["FTM"]=df["PLAYTYPE"].apply(lambda x: 1 if x=="FTM" else 0)
    df["O"]=df["PLAYTYPE"].apply(lambda x: 1 if x=="O" else 0)
    df["FTA"]=df["PLAYTYPE"].apply(lambda x: 1 if x=="FTA" else 0)
    df["TO"]=df["PLAYTYPE"].apply(lambda x: 1 if x=="TO" else 0)
    df["D"]=df["PLAYTYPE"].apply(lambda x: 1 if x=="D" else 0)
    df.IsHomeTeam=df.IsHomeTeam.fillna(False)

    data_home=df[["Gamecode","MARKERTIME","PERIOD","lineup","FGA","FGM","3FGM","2FGM","FTM","O","TO","D","FTA","IsHomeTeam"]]
    data_home.IsHomeTeam=data_home.IsHomeTeam.astype(int).fillna(0)
    for i in ["FGA","FTA","FGM","O","TO","D"]:
        data_home[i]=data_home[i]*data_home.IsHomeTeam.astype(int).fillna(0)
    for i in ["3FGM","2FGM","FTM"]:
        data_home[i+"_self"]=data_home[i]*data_home.IsHomeTeam
        data_home[i+"_opp"]=-data_home[i]*(data_home.IsHomeTeam-1)

    st.write(data_home)

    #st.write(data_home)

    df["lineup"]=df["Lineup_B"].apply(lambda x: "_".join(sorted(eval(x))))
    data_vis=df[["Gamecode","MARKERTIME","PERIOD","lineup","FGA","FGM","3FGM","2FGM","FTM","O","TO","D","FTA","IsHomeTeam"]]
    data_vis.IsHomeTeam=abs(data_home.IsHomeTeam.astype(int).fillna(0)-1)
    for i in ["FGA","FTA","FGM","O","TO","D"]:
        data_vis[i]=data_vis[i]*data_vis.IsHomeTeam.astype(int).fillna(0)
    for i in ["3FGM","2FGM","FTM"]:
        data_vis[i+"_self"]=data_vis[i]*data_vis.IsHomeTeam.astype(int).fillna(0)
        data_vis[i+"_opp"]=-data_vis[i]*(data_vis.IsHomeTeam.astype(int).fillna(0)-1)
    
    st.write(data_vis)

    data=pd.concat([data_home,data_vis])

    data=data[data.MARKERTIME==data.MARKERTIME]
    data["number"]=range(1,len(data)+1)
    
    data["lineup_n"] = (data['lineup'] != data['lineup'].shift()).cumsum()
    data["time"]=data.MARKERTIME.apply(lambda x: int(x.split(":")[0])*60+int(x.split(":")[1]))
    
    data=data.groupby(["Gamecode","PERIOD",'lineup_n']).agg({"lineup":"first", 
                         'time': lambda x: x.max() - x.min(),
                         "FGA":"sum",
                         "FGM":"sum",
                         "3FGM_self":"sum",
                         "2FGM_self":"sum",
                         "FTM_self":"sum",
                         "3FGM_opp":"sum",
                         "2FGM_opp":"sum",
                         "FTM_opp":"sum",
                         "O":"sum",
                         "D":"sum",
                         "TO":"sum",
                         "FTA":"sum"
                         })
    st.write(data)
    data=data[data.time>0]
    data=data.groupby("lineup", as_index=False).agg({"lineup":"first", 
                         'time': "sum",
                         "FGA":"sum",
                         "FGM":"sum",
                         "3FGM_self":"sum",
                         "2FGM_self":"sum",
                         "FTM_self":"sum",
                         "3FGM_opp":"sum",
                         "2FGM_opp":"sum",
                         "FTM_opp":"sum",
                         "O":"sum",
                         "D":"sum",
                         "TO":"sum",
                         "FTA":"sum"
                        })
    
    # extract possesions
    data["Points"]=3*data["3FGM_self"]+2*data["2FGM_self"]+data["FTM_self"]
    data["Points_opp"]=3*data["3FGM_opp"]+2*data["2FGM_opp"]+data["FTM_opp"]

    data["Poss1"]=data["FGA"]+0.44*data["FTA"]-data["O"]+data["TO"]
    data["Poss2"]=data["FGA"]+0.44*data["FTA"]-1.07*data["O"]/(data["O"]+data["D"])*(data["FGA"]-data["FGM"])+data["TO"]
    data["Pace1"]=data["Poss1"]/data["time"]*40*60
    data["Pace2"]=data["Poss2"]/data["time"]*40*60
    data["Off_rate"]=data["Points"]/data["Poss2"]*100
    data["Deff_rate"]=data["Points_opp"]/data["Poss2"]*100
    data["Net_rate"]=data["Off_rate"]-data["Deff_rate"]

    # extract   

    return(data)
