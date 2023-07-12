import pandas
import requests
import json

player_api_ids = pandas.read_excel('/Users/Matthew/Documents/GitHub/yfantasy-api/nhl-stats.xls', 'PlayerApiIds')
team_api_ids = pandas.read_excel('/Users/Matthew/Documents/GitHub/yfantasy-api/nhl-stats.xls', 'TeamApiIds')
draft = pandas.read_excel('/Users/Matthew/Documents/GitHub/yfantasy-api/nhl-stats.xls', 'Draft')
season1920 = pandas.read_excel('/Users/Matthew/Documents/GitHub/yfantasy-api/nhl-stats.xls', 'Season2019')
season2021 = pandas.read_excel('/Users/Matthew/Documents/GitHub/yfantasy-api/nhl-stats.xls', 'Season2020')
season2122 = pandas.read_excel('/Users/Matthew/Documents/GitHub/yfantasy-api/nhl-stats.xls', 'Season2021')

#get a data frame with selected columns
FORMAT = ['Player', 'Age', 'GP']

def get_player_gp_csv(player_name, season):
    df = get_season_sheet(season)
    df_selected = df[FORMAT]

    player_gp = -1
    try:
        result = df_selected.loc[df['Player'] == player_name, 'GP']
        player_gp = result.values[0]
    except:
        print(f'****** ERROR GETTING {player_name} GP in SEASON {season} from CSV ******')
    return player_gp

def get_player_id_csv(player_name):
    df = player_api_ids
    ID_FORMAT = ['Player', 'Id']
    df_selected = df[ID_FORMAT]

    player_api_id = -1
    try:
        result = df_selected.loc[df['Player'] == player_name, 'Id']
        player_api_id = result.values[0]
    except:
        print(f'****** ERROR GETTING {player_name} Id from CSV ******')
    
    if player_api_id == -1:
        try:
            response = requests.get("https://suggest.svc.nhl.com/svc/suggest/v1/minplayers/" + player_name + "/1")
            json_result = json.loads(response.text)
            player_data = json_result["suggestions"][0]
            player_api_id = player_data.split('|')[0]
        except:
            print(f'****** ERROR GETTING {player_name} Id from API ******')

    return player_api_id

def get_team_id_csv(team_name):
    df = team_api_ids
    ID_FORMAT = ['Team', 'Id']
    df_selected = df[ID_FORMAT]

    team_api_id = -1
    try:
        result = df_selected.loc[df['Team'] == team_name, 'Id']
        team_api_id = result.values[0]
    except:
        print(f'****** ERROR GETTING {team_name} Id from CSV ******')
    
    # SEE https://statsapi.web.nhl.com/api/v1/teams/ to get team Ids

    return team_api_id


def get_player_draft_csv(player_name):
    df = draft
    ID_FORMAT = ['Year', 'Round', 'Number', 'Drafted By', 'Player', 'ID', 'Pos', 'Drafted From']
    df_selected = df[ID_FORMAT]

    player_id = get_player_id_csv(player_name)
    draft_round = -1
    draft_number = -1

    try:
        result = df_selected.loc[df['ID'] == player_id, 'Round']
        draft_round = result.values[0]
        result = df_selected.loc[df['ID'] == player_id, 'Number']
        draft_number = result.values[0]
    except:
        draft_round = 1
        draft_number = -1
        #print(f'****** ERROR GETTING {player_name} DRAFT from CSV ******')

    draft_overall = (draft_round - 1) * 32 + draft_number

    return draft_overall

def get_season_sheet(season):
    if season == 2019:
        return season1920
    elif season == 2020:
        return season2021
    elif season == 2021:
        return season2122
    else:
        print(f'****** SEASON {season} NOT FOUND ******')

#print(get_player_gp('Connor McDavid', 2019))
#print(get_player_projected_points('Connor McDavid'))
#print(get_player_vorp('Connor McDavid'))