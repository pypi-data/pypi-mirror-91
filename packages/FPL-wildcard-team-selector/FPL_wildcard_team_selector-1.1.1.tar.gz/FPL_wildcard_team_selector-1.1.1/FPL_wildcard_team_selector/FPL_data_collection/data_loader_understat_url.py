import pandas as pd
import json
import requests
from bs4 import BeautifulSoup


def load_player_data_from_understat(understat_url:str, minimum_number_of_minutes_played:int):
    '''
    web scrapes all the relevant player information from the understat url.

    Parameters:
        understat_url (str): url to the understat page containing the players info

    Returns:
        players_info_df (DataFrame): Dataframe containing all the players stats 
    '''
    server_response = requests.get(understat_url)
    soup = BeautifulSoup(server_response.content, 'lxml')
    scripts = soup.find_all('script')
    players_info_text = scripts[3].string.strip()
    players_info_escape_sequences_ind_start = players_info_text.index("('") + 2 
    players_info_escape_sequences_ind_end = players_info_text.index("')")
    players_info_escape_sequences = players_info_text[players_info_escape_sequences_ind_start:players_info_escape_sequences_ind_end]
    decoded_players_info = players_info_escape_sequences.encode('utf8').decode('unicode_escape')
    players_info_dict = json.loads(decoded_players_info) 
    players_info_df = pd.DataFrame(players_info_dict)
    players_info_df = players_info_df.astype({'time':'float'})
    players_info_df = players_info_df[players_info_df['time'] > minimum_number_of_minutes_played]
    players_info_df.reset_index(inplace=True)
    return players_info_df


def load_teams_data_from_understat(understat_url:str):
    '''
    web scrapes all the relevant premier league teams information from the understat url.

    Parameters:
        understat_url (str): url to the understat page containing the teams info

    Returns:
        teams_info_df (DataFrame): Dataframe containing all the premier league teams stats 
    '''
    server_response = requests.get(understat_url)
    soup = BeautifulSoup(server_response.content, 'lxml')
    scripts = soup.find_all('script')
    teams_info_text = scripts[2].string.strip()
    teams_info_escape_sequences_ind_start = teams_info_text.index("('") + 2 
    teams_info_escape_sequences_ind_end = teams_info_text.index("')")
    teams_info_escape_sequences = teams_info_text[teams_info_escape_sequences_ind_start:teams_info_escape_sequences_ind_end]
    decoded_teams_info = teams_info_escape_sequences.encode('utf8').decode('unicode_escape')
    teams_info_dict = json.loads(decoded_teams_info)
    relevant_info_teams_info_dict = {}
    for key in teams_info_dict:
        team_name = teams_info_dict[key]['title']
        team_data = teams_info_dict[key]['history']
        stats_dict = {'xG':0, 'xGA':0, 'npxG':0, 'npxGA':0, 'npxGD':0, 'scored':0}
        for gameweek_dict in team_data:
            for key in stats_dict:
                stats_dict[key] = stats_dict[key] + gameweek_dict[key]
        stats_dict['npxGA90'] = stats_dict['npxGA'] / len(team_data)
        stats_dict['npxG90'] = stats_dict['npxG'] / len(team_data)
        stats_dict['xGA90'] = stats_dict['xGA'] / len(team_data)
        stats_dict['xG90'] = stats_dict['xG'] / len(team_data)
        relevant_info_teams_info_dict[team_name] = stats_dict
    teams_info_df = pd.DataFrame(relevant_info_teams_info_dict)
    return teams_info_df
