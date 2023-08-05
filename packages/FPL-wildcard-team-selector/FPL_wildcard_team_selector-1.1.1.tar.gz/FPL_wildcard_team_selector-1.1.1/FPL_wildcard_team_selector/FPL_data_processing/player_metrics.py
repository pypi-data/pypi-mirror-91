import pandas as pd
from FPL_wildcard_team_selector.FPL_data_collection import get_future_fixtures_info, fpl_teams_dict, load_teams_data_from_understat

def get_players_pts90(players_info):
    '''
    takes in a DataFrame containing all the players info, and adds a column series containing the 
    "pts per 90" metric which is: pts90 = (total pts * 90)/minutes 

    Parameters:
        players_info (DataFrame): DataFrame containing all the players info that was read from the main fantasy premier league API

    '''
    players_info.loc[:,'pts90'] = (players_info['total_points']/players_info['minutes']) * 90


def get_players_ROI(players_info):
    '''
    takes in a DataFrame containing all the players info, and adds a column series containing the 
    "return on investment" metric which is: ROI = (pts per 90 minutes)/cost 

    Parameters:
        players_info (DataFrame): DataFrame containing all the players info that was read from the main fantasy premier league API

    '''
    players_info.loc[:,'ROI'] = players_info['pts90']/players_info['now_cost']


def get_npxG90(players_info):
    '''
    takes in a DataFrame containing all the players info, and adds a column series containing the 
    "non penalty expected goals per 90" metric which is: npxG90 = (total npxG/total minutes) * 90 

    Parameters:
        players_info (DataFrame): DataFrame containing all the players info that was read from the main fantasy premier league API

    '''
    players_info.loc[:,'npxG90'] = (players_info['npxG'] * 90)/players_info['minutes']


def get_xG90(players_info):
    '''
    takes in a DataFrame containing all the players info, and adds a column series containing the 
    "expected goals per 90" metric which is: xG90 = (total xG/total minutes) * 90 

    Parameters:
        players_info (DataFrame): DataFrame containing all the players info that was read from the main fantasy premier league API

    '''
    players_info.loc[:,'xG90'] = (players_info['xG'] * 90)/players_info['minutes']


def get_G90(players_info):
    '''
    takes in a DataFrame containing all the players info, and adds a column series containing the 
    "goals per 90" metric which is: G90 = (total goals scored/total minutes) * 90 

    Parameters:
        players_info (DataFrame): DataFrame containing all the players info that was read from the main fantasy premier league API

    '''
    players_info.loc[:,'G90'] = (players_info['goals_scored'] * 90)/players_info['minutes']


def get_npg90(players_info):
    '''
    takes in a DataFrame containing all the players info, and adds a column series containing the 
    "non penalty expected goals per 90" metric which is: npg90 = (total npg/total minutes) * 90 

    Parameters:
        players_info (DataFrame): DataFrame containing all the players info that was read from the main fantasy premier league API

    '''
    players_info.loc[:,'npG90'] = (players_info['npg'] * 90)/players_info['minutes']


def get_xA90(players_info):
    '''
    takes in a DataFrame containing all the players info, and adds a column series containing the 
    "expected assist per 90" metric which is: xA90 = (total xA/total minutes) * 90 

    Parameters:
        players_info (DataFrame): DataFrame containing all the players info that was read from the main fantasy premier league API

    '''
    players_info.loc[:,'xA90'] = (players_info['xA'] * 90)/players_info['minutes']


def get_A90(players_info):
    '''
    takes in a DataFrame containing all the players info, and adds a column series containing the 
    "assist per 90" metric which is: A90 = (total A/total minutes) * 90 

    Parameters:
        players_info (DataFrame): DataFrame containing all the players info that was read from the main fantasy premier league API

    '''
    players_info.loc[:,'A90'] = (players_info['assists'] * 90)/players_info['minutes']


def get_players_future_games_attacking_ease(players_info, Num_Future_Games_To_Analyze, account_for_penalties, fpl_fixtures_info_api_url:str, teams_info_understat_url:str):
    '''
    takes in a DataFrame containing all the players info, and adds a column series containing the 
    "future games score" metric which is a measure of the difficulty of the games coming up in the near future

    Parameters:
        players_info (DataFrame): DataFrame containing all the players info that was read from the main fantasy premier league API
        Num_Future_Games_To_Analyze(int): number of future games to analyze
        account_for_penalties (bool): whether to account for penalties taken when analyzing the stats
        fpl_fixtures_info_api_url (str): FPL api url for all fixture information
        teams_info_understat_url (str): understat api url for all teams information
    '''
    players_info.loc[:,'future games attacking ease'] = 0
    fixtures_info_df = get_future_fixtures_info(fpl_fixtures_info_api_url)
    teams_info_understat_url = load_teams_data_from_understat(teams_info_understat_url)
    Num_Players = len(players_info.index)
    for i in range(Num_Players):
        players_team = players_info.loc[i,'team']
        player_specific_fixtures_info_df = fixtures_info_df[(fixtures_info_df['team_a']==int(players_team)) | (fixtures_info_df['team_h']==int(players_team))]
        player_specific_Attacking_ease_list = []
        for j in range(Num_Future_Games_To_Analyze):
            home_team = player_specific_fixtures_info_df['team_h'].iloc[j]
            away_team = player_specific_fixtures_info_df['team_a'].iloc[j]
            if home_team == int(players_team):
                if account_for_penalties:
                    match_ease = ((players_info.loc[i, 'xG90'] * teams_info_understat_url.loc['xGA90',fpl_teams_dict[str(away_team)]])
                                + (players_info.loc[i, 'xA90'] * teams_info_understat_url.loc['xGA90',fpl_teams_dict[str(away_team)]]))
                else:
                    match_ease = ((players_info.loc[i, 'npxG90'] * teams_info_understat_url.loc['npxGA90',fpl_teams_dict[str(away_team)]])
                                + (players_info.loc[i, 'xA90'] * teams_info_understat_url.loc['npxGA90',fpl_teams_dict[str(away_team)]]))                   
            elif away_team == int(players_team):
                if account_for_penalties:
                    match_ease = ((players_info.loc[i, 'xG90'] * teams_info_understat_url.loc['xGA90',fpl_teams_dict[str(home_team)]])
                                + (players_info.loc[i, 'xA90'] * teams_info_understat_url.loc['xGA90',fpl_teams_dict[str(home_team)]]))
                else:
                    match_ease = ((players_info.loc[i, 'npxG90'] * teams_info_understat_url.loc['npxGA90',fpl_teams_dict[str(home_team)]])
                                + (players_info.loc[i, 'xA90'] * teams_info_understat_url.loc['npxGA90',fpl_teams_dict[str(home_team)]]))                  
            else:
                raise ValueError("using corrupted data frames, please check your sources")
            player_specific_Attacking_ease_list.append(match_ease)
        fixtures_defending_ease_mean = sum(player_specific_Attacking_ease_list) / len(player_specific_Attacking_ease_list)
        players_info.loc[i,'future games attacking ease'] = fixtures_defending_ease_mean


def get_players_future_games_defending_ease(players_info, Num_Future_Games_To_Analyze, account_for_penalties, fpl_fixtures_info_api_url:str, teams_info_understat_url:str):
    '''
    takes in a DataFrame containing all the players info, and adds a column series containing the 
    "future games score" metric which is a measure of the difficulty of the games coming up in the near future

    Parameters:
        players_info (DataFrame): DataFrame containing all the players info that was read from the main fantasy premier league API
        Num_Future_Games_To_Analyze(int): number of future games to analyze
        account_for_penalties (bool): whether to account for penalties taken when analyzing the stats
        fpl_fixtures_info_api_url (str): FPL api url for all fixture information
        teams_info_understat_url (str): understat api url for all teams information
    '''
    players_info.loc[:,'future games defending ease'] = 0
    fixtures_info_df = get_future_fixtures_info(fpl_fixtures_info_api_url)
    teams_info_understat_url = load_teams_data_from_understat(teams_info_understat_url)
    future_fixtures_defending_ease_dict = {}

    for key in fpl_teams_dict:
        team_specific_fixtures_info_df = fixtures_info_df[(fixtures_info_df['team_a']==int(key)) | (fixtures_info_df['team_h']==int(key))]
        team_specific_defending_ease_list = []
        for i in range(Num_Future_Games_To_Analyze):
            home_team = team_specific_fixtures_info_df['team_h'].iloc[i]
            away_team = team_specific_fixtures_info_df['team_a'].iloc[i]
            if home_team == int(key):
                if account_for_penalties:
                    match_ease = 1/(teams_info_understat_url.loc['xGA90',fpl_teams_dict[str(home_team)]] * teams_info_understat_url.loc['xG90',fpl_teams_dict[str(away_team)]])
                else:
                    match_ease = 1/(teams_info_understat_url.loc['npxGA90',fpl_teams_dict[str(home_team)]] * teams_info_understat_url.loc['npxG90',fpl_teams_dict[str(away_team)]])
            elif away_team == int(key):
                if account_for_penalties:
                    match_ease = 1/(teams_info_understat_url.loc['xGA90',fpl_teams_dict[str(away_team)]] * teams_info_understat_url.loc['xG90',fpl_teams_dict[str(home_team)]])
                else:
                    match_ease = 1/(teams_info_understat_url.loc['npxGA90',fpl_teams_dict[str(away_team)]] * teams_info_understat_url.loc['npxG90',fpl_teams_dict[str(home_team)]])
            else:
                raise ValueError("using corrupted data frames, please check your sources")
            team_specific_defending_ease_list.append(match_ease)
        fixtures_defending_ease_mean = sum(team_specific_defending_ease_list) / len(team_specific_defending_ease_list)
        future_fixtures_defending_ease_dict[key] = fixtures_defending_ease_mean

    Num_Players = len(players_info.index)
    for i in range(Num_Players):
        players_team = players_info.loc[i,'team']
        players_next_n_games_defending_ease_mean = future_fixtures_defending_ease_dict[str(players_team)]
        players_info.loc[i,'future games defending ease'] = players_next_n_games_defending_ease_mean


def get_chance_conversion_ability(players_info, account_for_penalties):
    '''
    takes in a DataFrame containing all the players info, and adds a column series containing the 
    "chance_conversion_ability" metric which is: 
        chance_conversion_ability = G90 - xG90 , if we account for penalties
        chance_conversion_ability = npG90 - npxG90 , if we dont account for penalties

    Parameters:
        players_info (DataFrame): DataFrame containing all the players info that was read from the main fantasy premier league API
        account_for_penalties (bool): whether to account for penalties taken when analyzing the stats

    '''
    if account_for_penalties:
        players_info.loc[:,'chance_conversion_ability'] = players_info['G90'] - players_info['xG90']
        players_info.sort_values(by='chance_conversion_ability', inplace = True, ascending=True)
        Lowest_Value_In_Col = players_info['chance_conversion_ability'].values[0]
        players_info.sort_values(by='chance_conversion_ability', inplace = True, ascending=False)
        Highest_Value_In_Col = players_info['chance_conversion_ability'].values[0]

        players_info.loc[:,'chance_conversion_ability'] = (players_info['chance_conversion_ability'] - Lowest_Value_In_Col)/(Highest_Value_In_Col - Lowest_Value_In_Col)
        players_info.loc[players_info['xG90']==0, 'chance_conversion_ability'] = 0
        players_info.loc[players_info['G90']==0, 'chance_conversion_ability'] = 0
    else:
        players_info.loc[:,'chance_conversion_ability'] = players_info['npG90'] - players_info['npxG90']
        players_info.sort_values(by='chance_conversion_ability', inplace = True, ascending=True)
        Lowest_Value_In_Col = players_info['chance_conversion_ability'].values[0]
        players_info.sort_values(by='chance_conversion_ability', inplace = True, ascending=False)
        Highest_Value_In_Col = players_info['chance_conversion_ability'].values[0]

        players_info.loc[:,'chance_conversion_ability'] = (players_info['chance_conversion_ability'] - Lowest_Value_In_Col)/(Highest_Value_In_Col - Lowest_Value_In_Col)
        players_info.loc[players_info['npxG90']==0, 'chance_conversion_ability'] = 0
        players_info.loc[players_info['npG90']==0, 'chance_conversion_ability'] = 0


def get_assisting_ability(players_info):
    '''
    takes in a DataFrame containing all the players info, and adds a column series containing the 
    "assisting_ability" metric which is: assisting_ability = A90 - xA90 

    Parameters:
        players_info (DataFrame): DataFrame containing all the players info that was read from the main fantasy premier league API

    '''
    players_info.loc[:,'assisting_ability'] = players_info['A90'] - players_info['xA90']
    players_info.sort_values(by='assisting_ability', inplace = True, ascending=True)
    Lowest_Value_In_Col = players_info['assisting_ability'].values[0]
    players_info.sort_values(by='assisting_ability', inplace = True, ascending=False)
    Highest_Value_In_Col = players_info['assisting_ability'].values[0]

    players_info.loc[:,'assisting_ability'] = (players_info['assisting_ability'] - Lowest_Value_In_Col)/(Highest_Value_In_Col - Lowest_Value_In_Col)
    players_info.loc[players_info['xA90']==0, 'assisting_ability'] = 0
    players_info.loc[players_info['A90']==0, 'assisting_ability'] = 0
