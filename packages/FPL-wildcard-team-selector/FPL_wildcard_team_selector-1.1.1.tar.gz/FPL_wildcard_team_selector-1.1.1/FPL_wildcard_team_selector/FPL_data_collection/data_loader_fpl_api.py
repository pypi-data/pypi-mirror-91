import pandas as pd
import json
import requests


def load_json_data_from_FPL_url(url:str):
    '''
    sends a Get request to the specified Fantasy Premier League url and returns the received json string as a dictionary. 

    Returns:
        data (dict): dictionary containing all the data from the url 
    '''
    server_response = requests.get(url) 
    data = json.loads(server_response.content)
    return data


def parse_main_FPL_API(fpl_main_api_url:str):
    '''
    takes in all the data from the main Fantasy premier league API, and returns the most important data as DataFrames.

    The response from the FPL main API should be a json string with 8 main attributes:
    elements, element_stats, element_types, events, game_settings, phases, teams, total_players

    The most valuable info are in : elements, events, and teams
    elements: Player summary data such as total points and costs
    events: gameweek data such as id, deadline time, and highest scoring player
    Teams: Data for each team such as name, and id as well as scores for the team attack, defence, overall when home and away

    Parameters:
        FPL_API_data_dict (dict): dictionary containing all the data from the fantasy premier league main API

    Returns:
        players_df (DataFrame): pandas DataFrame containing all the data about the players from the input dictionary
        teams_df (DataFrame): pandas DataFrame containing all the data about the premier league teams from the input dictionary
    '''
    FPL_API_data_dict = load_json_data_from_FPL_url(fpl_main_api_url)
    players = FPL_API_data_dict['elements']
    teams = FPL_API_data_dict['teams']

    players_df = pd.DataFrame(players)
    players_df = players_df[['id','first_name','second_name','web_name','element_type',
                            'team','minutes','goals_scored','assists','goals_conceded',
                            'now_cost','ep_next','form','total_points','ict_index',
                            'points_per_game','chance_of_playing_next_round']]
    teams_df = pd.DataFrame(teams)
    return players_df, teams_df


def get_future_fixtures_info(fpl_fixtures_info_api_url:str):
    '''
    This function collects the future fixture information for all the clubs in the premier league

    Parameters:
        fpl_fixtures_info_api_url (str): FPL api url for all fixture information

    Returns:
        fixtures_info_df (DataFrame): pandas DataFrame containing all the details about the upcoming fixtures for the premier league teams
    '''
    fixtures_info_dict = load_json_data_from_FPL_url(fpl_fixtures_info_api_url)
    fixtures_info_df = pd.DataFrame(fixtures_info_dict)
    fixtures_info_df = fixtures_info_df[fixtures_info_df['started']==False]
    return fixtures_info_df
