import pandas as pd
from .utilities import set_range_one_to_ten


def calculate_players_scores_weighted_avg_sum(players_info, strikers_midfielders_scoring_weights, defenders_goalies_scoring_weights, players_info_csv):
    '''
    takes in a DataFrame containing all the players info and stats, and two lists containing all the weights that will be used in the 
    weighted sum. Adds a column called Algorithm Score to the existing Dataframe which is the final score out of 10 given to each player

    Parameters:
        players_info (DataFrame): DataFrame containing all the players info that was read from the main fantasy premier league API
        defenders_goalies_scoring_weights (list): list containing the weights of [Future games attacking ease, Future games defending ease, chance conversion ability, assisting ability, ROI] in that order for defenders and goalies
        strikers_midfielders_scoring_weights (list): list containing the weights of [Future games attacking ease, Future games defending ease, chance conversion ability, assisting ability, ROI] in that order for strikers and midfielders

    '''
    columns_to_normalize = ['future games attacking ease', 'future games defending ease', 'chance_conversion_ability', 'assisting_ability', 'ROI', 'pts90']
    set_range_one_to_ten(players_info, columns_to_normalize)

    #Future games attacking ease, Future games defending ease, chance conversion ability, assisting ability, ROI
    defenders_goalies_scoring_weights_sum = (defenders_goalies_scoring_weights[0] + defenders_goalies_scoring_weights[1]
                                             + defenders_goalies_scoring_weights[2] + defenders_goalies_scoring_weights[3]
                                             + defenders_goalies_scoring_weights[4] + defenders_goalies_scoring_weights[5])
    strikers_midfielders_scoring_weights_sum = (strikers_midfielders_scoring_weights[0] + strikers_midfielders_scoring_weights[1]
                                             + strikers_midfielders_scoring_weights[2] + strikers_midfielders_scoring_weights[3]
                                             + strikers_midfielders_scoring_weights[4] + strikers_midfielders_scoring_weights[5])

    players_info.loc[:,'Algorithm Score'] = 0

    players_info.loc[players_info['element_type'] == 1,'Algorithm Score'] = (
                                        (players_info['future games attacking ease'].multiply(defenders_goalies_scoring_weights[0]))                         
                                        + (players_info['future games defending ease'].multiply(defenders_goalies_scoring_weights[1]))
                                        + (players_info['chance_conversion_ability'].multiply(defenders_goalies_scoring_weights[2]))
                                        + (players_info['assisting_ability'].multiply(defenders_goalies_scoring_weights[3]))
                                        + (players_info['ROI'].multiply(defenders_goalies_scoring_weights[4]))
                                        + (players_info['pts90'].multiply(defenders_goalies_scoring_weights[5]))) / defenders_goalies_scoring_weights_sum

    players_info.loc[players_info['element_type'] == 2,'Algorithm Score'] = (
                                        (players_info['future games attacking ease'].multiply(defenders_goalies_scoring_weights[0]))                         
                                        + (players_info['future games defending ease'].multiply(defenders_goalies_scoring_weights[1]))
                                        + (players_info['chance_conversion_ability'].multiply(defenders_goalies_scoring_weights[2]))
                                        + (players_info['assisting_ability'].multiply(defenders_goalies_scoring_weights[3]))
                                        + (players_info['ROI'].multiply(defenders_goalies_scoring_weights[4]))
                                        + (players_info['pts90'].multiply(defenders_goalies_scoring_weights[5]))) / defenders_goalies_scoring_weights_sum

    players_info.loc[players_info['element_type'] == 3,'Algorithm Score'] = (
                                        (players_info['future games attacking ease'].multiply(strikers_midfielders_scoring_weights[0]))                         
                                        + (players_info['future games defending ease'].multiply(strikers_midfielders_scoring_weights[1]))
                                        + (players_info['chance_conversion_ability'].multiply(strikers_midfielders_scoring_weights[2]))
                                        + (players_info['assisting_ability'].multiply(strikers_midfielders_scoring_weights[3]))
                                        + (players_info['ROI'].multiply(strikers_midfielders_scoring_weights[4]))
                                        + (players_info['pts90'].multiply(strikers_midfielders_scoring_weights[5]))) / strikers_midfielders_scoring_weights_sum

    players_info.loc[players_info['element_type'] == 4,'Algorithm Score'] = (
                                        (players_info['future games attacking ease'].multiply(strikers_midfielders_scoring_weights[0]))                         
                                        + (players_info['future games defending ease'].multiply(strikers_midfielders_scoring_weights[1]))
                                        + (players_info['chance_conversion_ability'].multiply(strikers_midfielders_scoring_weights[2]))
                                        + (players_info['assisting_ability'].multiply(strikers_midfielders_scoring_weights[3]))
                                        + (players_info['ROI'].multiply(strikers_midfielders_scoring_weights[4]))
                                        + (players_info['pts90'].multiply(strikers_midfielders_scoring_weights[5]))) / strikers_midfielders_scoring_weights_sum
    
    players_info_csv.loc[:,'Algorithm Score'] = players_info.loc[:,'Algorithm Score']
    players_info_csv.sort_values(by='Algorithm Score', inplace = True, ascending=False) 
    players_info.sort_values(by='Algorithm Score', inplace = True, ascending=False) 
