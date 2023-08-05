import FPL_wildcard_team_selector.FPL_data_collection as dc
import FPL_wildcard_team_selector.FPL_data_processing as dp
import FPL_wildcard_team_selector.FPL_data_visualization as dv
import pandas as pd
import os

def play_wildcard(money_available=100, minimum_number_of_minutes_played=630, number_of_future_games_to_analyze=3, account_for_penalties=True):
    fpl_main_api_url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    fpl_fixtures_info_api_url = 'https://fantasy.premierleague.com/api/fixtures/'
    understat_players_and_teams_info_url = 'https://understat.com/league/EPL/2020'
    
    print(" currently selecting the best 15 players for your wildcard, please be patient. This may take a few seconds")
    fpl_players_info, fpl_teams_info = dc.parse_main_FPL_API(fpl_main_api_url)
    understat_players_info = dc.load_player_data_from_understat(understat_players_and_teams_info_url, minimum_number_of_minutes_played)
    dc.combine_data_from_fpl_understat(fpl_players_info,understat_players_info)

    fpl_players_info = fpl_players_info[(fpl_players_info['minutes'] > minimum_number_of_minutes_played) & (fpl_players_info['chance_of_playing_next_round'] != 0)]
    fpl_players_info.reset_index(inplace=True)

    columns_to_turn_to_floats = ['form','points_per_game','ict_index','ep_next', 'npxG', 'xA','xG','npg','assists']
    fpl_players_info = dp.turn_series_to_float(fpl_players_info, columns_to_turn_to_floats)

    dp.add_players_full_name(fpl_players_info)
    dp.get_players_pts90(fpl_players_info)
    dp.get_players_ROI(fpl_players_info)
    dp.get_G90(fpl_players_info)
    dp.get_xG90(fpl_players_info)
    dp.get_npxG90(fpl_players_info)
    dp.get_npg90(fpl_players_info)
    dp.get_A90(fpl_players_info)
    dp.get_xA90(fpl_players_info)
    dp.get_assisting_ability(fpl_players_info)
    dp.get_chance_conversion_ability(fpl_players_info, account_for_penalties)
    dp.get_players_future_games_defending_ease(fpl_players_info, number_of_future_games_to_analyze, account_for_penalties, fpl_fixtures_info_api_url, understat_players_and_teams_info_url)
    dp.get_players_future_games_attacking_ease(fpl_players_info, number_of_future_games_to_analyze, account_for_penalties, fpl_fixtures_info_api_url, understat_players_and_teams_info_url)
    fpl_players_info_csv = fpl_players_info.copy()
    #Future games attacking ease, Future games defending ease, chance conversion ability, assisting ability, ROI, pts90
    srikers_midfielders_scoring_weights = [0.5, 0.0, 0.2, 0.1, 0.0, 0.2] 
    defenders_goalies_scoring_weights = [0.3, 0.4, 0.05, 0.05, 0.2, 0.0]

    dp.calculate_players_scores_weighted_avg_sum(fpl_players_info, srikers_midfielders_scoring_weights, defenders_goalies_scoring_weights, fpl_players_info_csv)
    ListOfGoalies, ListOfDef, ListOfMid, ListOfStr, Cash_Left = dp.team_selection_using_linear_optimization(fpl_players_info, (money_available*10))

    visualization_object = dv.visualize_team_selection(ListOfGoalies, ListOfDef, ListOfMid, ListOfStr, Cash_Left)
    print(" Team selection is done. To exit the program, you can close the graphics tab")
    visualization_object.run_visualization()


def generate_player_stats(minimum_number_of_minutes_played=630, number_of_future_games_to_analyze=3, account_for_penalties=True):
    fpl_main_api_url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    fpl_fixtures_info_api_url = 'https://fantasy.premierleague.com/api/fixtures/'
    understat_players_and_teams_info_url = 'https://understat.com/league/EPL/2020'
    
    print(" currently generating detailed stats on all the players, please be patient. This may take a few seconds")
    fpl_players_info, fpl_teams_info = dc.parse_main_FPL_API(fpl_main_api_url)
    understat_players_info = dc.load_player_data_from_understat(understat_players_and_teams_info_url, minimum_number_of_minutes_played)
    dc.combine_data_from_fpl_understat(fpl_players_info,understat_players_info)

    fpl_players_info = fpl_players_info[(fpl_players_info['minutes'] > minimum_number_of_minutes_played) & (fpl_players_info['chance_of_playing_next_round'] != 0)]
    fpl_players_info.reset_index(inplace=True)

    columns_to_turn_to_floats = ['form','points_per_game','ict_index','ep_next', 'npxG', 'xA','xG','npg','assists']
    fpl_players_info = dp.turn_series_to_float(fpl_players_info, columns_to_turn_to_floats)

    dp.add_players_full_name(fpl_players_info)
    dp.get_players_pts90(fpl_players_info)
    dp.get_players_ROI(fpl_players_info)
    dp.get_G90(fpl_players_info)
    dp.get_xG90(fpl_players_info)
    dp.get_npxG90(fpl_players_info)
    dp.get_npg90(fpl_players_info)
    dp.get_A90(fpl_players_info)
    dp.get_xA90(fpl_players_info)
    dp.get_assisting_ability(fpl_players_info)
    dp.get_chance_conversion_ability(fpl_players_info, account_for_penalties)
    dp.get_players_future_games_defending_ease(fpl_players_info, number_of_future_games_to_analyze, account_for_penalties, fpl_fixtures_info_api_url, understat_players_and_teams_info_url)
    dp.get_players_future_games_attacking_ease(fpl_players_info, number_of_future_games_to_analyze, account_for_penalties, fpl_fixtures_info_api_url, understat_players_and_teams_info_url)
    fpl_players_info_csv = fpl_players_info.copy()
    #Future games attacking ease, Future games defending ease, chance conversion ability, assisting ability, ROI, pts90
    srikers_midfielders_scoring_weights = [0.5, 0.0, 0.2, 0.1, 0.0, 0.2] 
    defenders_goalies_scoring_weights = [0.3, 0.4, 0.05, 0.05, 0.2, 0.0]

    dp.calculate_players_scores_weighted_avg_sum(fpl_players_info, srikers_midfielders_scoring_weights, defenders_goalies_scoring_weights, fpl_players_info_csv)
    
    columns_to_normalize_for_csv = ['future games attacking ease', 'future games defending ease', 'chance_conversion_ability', 'assisting_ability', 'ROI']
    dp.set_range_one_to_ten(fpl_players_info_csv, columns_to_normalize_for_csv)
    fpl_players_info_csv.sort_values(by='Algorithm Score', inplace = True, ascending=False)
    fpl_players_info_csv.loc[:,'now_cost'] = fpl_players_info_csv['now_cost'] * 0.1

    list_of_df = []
    for i in range(1,5):
        list_of_df.append(fpl_players_info_csv[fpl_players_info_csv['element_type']==i])

    csv_path = os.path.join(os.getcwd(),'FPL_detailed_players_stats.csv')
    columns_to_add_to_csv = ['web_name','now_cost','total_points','pts90','ROI','minutes','goals_scored','npg','xG', 'npxG',
                            'npxG90', 'npG90', 'xG90', 'G90', 'chance_conversion_ability', 'assists','xA', 'xA90', 'A90',
                            'assisting_ability','future games attacking ease', 'future games defending ease', 'Algorithm Score']

    with open(csv_path,'w+',encoding='utf-8') as f:
        for df in reversed(list_of_df):
            df[columns_to_add_to_csv].to_csv(f, float_format='%.2f',index=False, line_terminator='\n')
            f.write("\n")
        f.close()

    print(" Player stats generation is done. You can find a csv containing all the detailed stats on all the players in the following path:\n {path}".format(path=csv_path))
