from yfantasy_api.api import YahooFantasyApi
from FantasyProjections import get_player_age, get_player_projected_points
from DraftPickValues import get_draft_pick_value, pick_value_round_1
from NHLStats import get_player_gp_csv, get_player_draft_csv
from RetrieveStatsApi import get_player_stats_api, get_team_gp_api
from yfantasy_api.models import transaction
from TeamRank import TeamRank, PlayerRank
import csv

league_id = 610  # This should be the id of the league you are querying
game_id = 'nhl'    # This should be the id of the game you are querying
team_id = 1        # This should be the id of the team you are querying

inital_trade_difference_level = 30 # number of rank points for trade to be acceptable within
commish_decision_level = 10 # number of rank points after trade difference for it to be left up to commish
#current_rank_multipler = 1 # number to multiply current rank by
impact_player_val = 5

replacement_forward_rank = 255 # rank of a replacement level foward
replacement_centre_rank = 280 # rank of a replacemet c
replacement_lw_rank = 257 # rank of a replacement lw
replacement_rw_rank = 252 # rank of a replacement rw
replacement_defence_rank = 216 # rank of a replacement level foward
replacement_goalie_rank = 182 # rank of a replacement level goalie
#replacement_goalie_rank = 178 # rank of a replacement level goalie
#replacement_player_rank = ((replacement_forward_rank * 9) + (replacement_defence_rank * 4) + (replacement_defence_rank * 3)) / 16 
replacement_player_rank = 229 # rank of a replacement player
keeper_player_rank = 330 # rank of the lowest level keeper player
injured_season_rank = 155 # this is variable to identify when to scrap the points collected by player in a season

number_of_games_in_current_season = 82 # number of current games in current season so we can find FP projection of players
seasons_back = 3 # number of seasons to go back into calculations

injured_statuses = ["IR-LT", "IR", "O", "DTD"]

show_year_by_year_stats = True # turn to True to see year by year breakdown
show_trade_difference_level = False # turn to True to see year by year breakdown
apply_player_depreciation = False # turn to True to apply player depreciation as season goes on
print_just_vals = "Blank" # turn to Nothing, Blank, CSV or Just Vals print the Rich Vals

api = YahooFantasyApi(league_id, game_id)

league = api \
    .league() \
    .get()

leagueTeams = api \
    .league() \
    .teams() \
    .get()

def get_player_rank(player, print_vals = "Blank", writer=None):
    if player.isnumeric():
        pick_rank = get_draft_pick_value(player)

        # take VORP into account
        pick_rank -= replacement_player_rank

        if print_vals != "Just Vals" and print_vals != "Nothing":
            print(f'DRAFT PICK ROUND {player} VALUE -- {pick_rank}')

        return pick_rank
    else:
        try:
            # add current points + projected points to player rank
            player_rank = 0
            player_position = ''
            player_injury_status = ''
            #player_current_rank_multipler = current_rank_multipler
            player_current_rank_multipler = 1
            player_age = get_player_age(player)
            player_projected_points = get_player_projected_points(player)
            
            current_nhl_team_gp = 0
            player_draft_overall = get_player_draft_csv(player)

            for seasons_removed in range(0, seasons_back):
                cur_season = league.season - seasons_removed

                stats = api \
                    .league() \
                    .players(search=player) \
                    .stats(season=cur_season) \
                    .get()

                player_position = stats.players[0].position

                #####################################################################################
                #points = stats.players[0].points

                is_goalie = player_position == "G"
                player_stats = get_player_stats_api(player, is_goalie, cur_season)
                points = player_stats.get_fantasy_points()
                #####################################################################################

                if player_projected_points == -1:
                    player_projected_points = get_replacement_rank(player_position) * 0.85
                player_injury_status = stats.players[0].status # can be None, IR, IR-LT, DTD, O
                player_nhl_team = stats.players[0].nhl_team
                player_gp = 0
                nhl_team_gp = 0
                if seasons_removed != 0:
                    player_gp = get_player_gp_csv(player, cur_season)
                if seasons_removed == 0:
                    player_gp = player_stats.gp
                    #player_gp = get_player_gp_api(player, cur_season)
                    nhl_team_gp = get_team_gp_api(player_nhl_team)
                    current_nhl_team_gp = nhl_team_gp

                # adjust for goalies
                combined_gp = player_gp if player_position != "G" else nhl_team_gp

                if seasons_removed == 0:
                    # change player_current_rank_multipler based on how many 
                    if combined_gp >= 0 and combined_gp < 10:
                        player_current_rank_multipler = 1 # set to 1 because we will just take projected points
                    else:
                        player_current_rank_multipler = min(combined_gp/25, 2)
                    #elif combined_gp >= 10 and combined_gp < 20:
                    #    player_current_rank_multipler = 0.5
                    #elif combined_gp >= 20 and combined_gp < 30:
                    #    player_current_rank_multipler = 1
                    #elif combined_gp >= 30 and combined_gp < 42:
                    #    player_current_rank_multipler = 1.5
                    #elif combined_gp >= 42:
                    #    player_current_rank_multipler = 2
                
                    # if a player is very young then put more emphasis on current season
                    if ((player_position == "G" and player_age < 25) or player_age < 23) and is_below_keeper_rank(points*82/combined_gp - 20, player_position):
                        player_current_rank_multipler = player_current_rank_multipler * 2
                
                # if we are in current year then calculate what player will get to on current pace
                # and add multipler to give this year presendence
                if seasons_removed == 0 and (combined_gp < 10 or (player_position == "G" and player_gp < 9)):
                    points = player_projected_points * player_current_rank_multipler
                elif seasons_removed == 0:
                    #points *= 82 / combined_gp * player_current_rank_multipler
                    points_this_season = points * 82 / combined_gp * player_current_rank_multipler

                    # if player is in realistic range then put more emphasis on this season
                    if player_current_rank_multipler < 2 and combined_gp > 10 and combined_gp < 25 and \
                        player_injury_status not in injured_statuses and points_this_season / player_current_rank_multipler > injured_season_rank and \
                        points_this_season / player_current_rank_multipler < player_projected_points + 75:
                        player_current_rank_multipler += 0.25
                    
                    points *= 82 / combined_gp * player_current_rank_multipler

#######################################################################################################
                # need to adjust for shortened season in 2019
                if cur_season == 2019:
                    points *= 82 / 70
                
                # need to adjust for shortened season in 2020
                if cur_season == 2020:
                    points *= 82 / 56
                
                #if cur_season == 2022:
                #    points = get_player_projected_points(player) * player_current_rank_multipler

#######################################################################################################
                # need to handle cases when the points in a given year is less than 100 due to injury
                if player_gp > 0 and player_position != "G" and seasons_removed != 0 and ((cur_season == 2020 and player_gp < 36) or (cur_season != 2020 and player_gp < 50)):
                    if cur_season == 2020:
                        points = points / player_gp * 82 * 0.85
                    else:
                        points = points / player_gp * 82 * 0.85
                elif (points < injured_season_rank and seasons_removed != 0) or (points < player_projected_points / 2.2 and seasons_removed != 0):
                    points = player_projected_points * 0.85

                #if seasons_removed == 0 and player_injury_status == "IR-LT":
                #    points = get_player_projected_points(player) * player_current_rank_multipler * 0.7
                #if seasons_removed == 0 and player_injury_status == "IR":
                #    points = get_player_projected_points(player) * player_current_rank_multipler * 0.85
                #elif seasons_removed == 0 and player_injury_status == "O":
                #    points = get_player_projected_points(player) * player_current_rank_multipler * 0.90
                #elif seasons_removed == 0 and player_injury_status == "DTD":
                #    points = points * player_current_rank_multipler * 0.95

                #if (points < injured_season_rank and r != 0) or (points < get_player_projected_points(player) / 2.2 and r != 0) or (points / player_current_rank_multipler < injured_season_rank and r == 0 and league.current_week / league.end_week >= 0.5):
                #    if r == 0:
                #        points = get_player_projected_points(player) * player_current_rank_multipler * 0.8
                #    else:
                #        points = get_player_projected_points(player) * 0.8
                    
                    ## if player was hurt for extended period then give him replacement level value
                    #if curr_rank / player_current_rank_multipler < injured_season_rank and r == 0:
                    #    player_current_rank_multipler = current_rank_multipler / 1.6
                    #    points = replacement_player_rank * player_current_rank_multipler
                    #    curr_rank = 0 # need to set curr_rank to 0 in case player has been injured multiple years
                    #elif curr_rank / player_current_rank_multipler < injured_season_rank and r != 0:
                    #    points = replacement_player_rank
                    #else:
                    #    points = curr_rank / player_current_rank_multipler * 0.8

                if show_year_by_year_stats:
                    printPoints = points if seasons_removed != 0 else points / player_current_rank_multipler
                    if seasons_removed != 0:
                        print(f'{cur_season} - {printPoints}')
                    else:
                        print(f'{cur_season} - {printPoints} (x{player_current_rank_multipler})')
                
                player_rank += points
            
            # add in Dom's projected points
            player_rank += player_projected_points
            
            if show_year_by_year_stats:
                print(f'ProjP - {player_projected_points}') # Uncomment to see Dom's projected points

            # divide player_rank by 4 to take an average of last n years + projected points
            player_rank /= (seasons_back + 1 + player_current_rank_multipler - 1)

            if show_year_by_year_stats:
                print(f'PreAdjRank - {player_rank}')
                print(f'Injury Status - {player_injury_status}')

            # add player age multipler
            age_multiplier = 1

            if not is_below_keeper_rank(player_rank, player_position):
                if player_age > 35:
                    age_multiplier = 0.95
                elif player_age >= 32 and player_age <= 35:
                    age_multiplier = 0.97
                elif player_age >= 30 and player_age <= 31:
                    age_multiplier = 0.99
                elif player_age >= 23 and player_age <= 24:
                    age_multiplier = 1.02
                elif player_age >= 20 and player_age <= 22:
                    age_multiplier = 1.045
                elif player_age < 20:
                    age_multiplier = 1.07
            else:
                if player_age > 35:
                    age_multiplier = 0.97
                elif player_age >= 32 and player_age <= 35:
                    age_multiplier = 0.98
                elif player_age >= 30 and player_age <= 31:
                    age_multiplier = 0.99
                elif player_age >= 23 and player_age <= 24:
                    age_multiplier = 1.03
                elif player_age >= 20 and player_age <= 22:
                    age_multiplier = 1.07
                elif player_age < 20:
                    age_multiplier = 1.12
            
            if player_draft_overall > 0 and player_age < 23 and is_below_keeper_rank(player_rank - 20, player_position):
                if player_draft_overall == 1:
                    age_multiplier += 0.05
                elif player_draft_overall <= 3:
                    age_multiplier += 0.035
                elif player_draft_overall <= 5:
                    age_multiplier += 0.025
                elif player_draft_overall <= 10:
                    age_multiplier += 0.02
            
            player_rank *= age_multiplier
            
            # subtract some player_rank if player is currently injured (not as heavy for keepers) 
            if not is_below_keeper_rank(player_rank, player_position):
                if player_injury_status in injured_statuses:
                    player_rank = player_rank * 0.95
            else:
                if player_injury_status == "IR-LT":
                    player_rank = player_rank * 0.85
                if player_injury_status == "IR":
                    player_rank = player_rank * 0.9
                elif player_injury_status == "O":
                    player_rank = player_rank * 0.95
                elif player_injury_status == "DTD":
                    player_rank = player_rank * 0.98

            if show_year_by_year_stats and print_vals != "Nothing":
                print(f'RankBeforeVORP - {player_rank}') # Uncomment to see player's projected rank before VORP

            pre_vorp_rank = player_rank

            # take VORP into account
            replacement_rank = get_replacement_rank(player_position)
            player_rank -= replacement_rank

            # take season value going down into effect
            if apply_player_depreciation and is_below_keeper_rank(player_rank+replacement_rank-20, player_position) and current_nhl_team_gp > 30:
                depreciation_val = max((110-current_nhl_team_gp)/80, 0.75)
                player_rank *= depreciation_val
            
            if player == "Alex Pietrangelo" or player == "Chris Kreider":
                player_rank -= 5
            
            # if player in trade's VORP is negative then just replace with replacement player
            if print_vals == "Just Vals":
                print(f'{player_rank}')
            elif print_vals == "Nothing":
                a = 1
            elif print_vals == "CSV":
                playerRow = [player, player_position, pre_vorp_rank, player_rank]
                writer.writerow(playerRow)
                print(f'{player} - {player_rank} just processed')
            else:
                if player_rank < 0:
                    print(f'{player} VALUE -- 0 (ACTUAL -- {player_rank})')
                    player_rank = 0
                else:
                    print(f'{player} VALUE -- {player_rank}')

            return player_rank
        except:
            print(f'****** ERROR PARSING {player} ******')

def is_below_keeper_rank(rank, position):
    p_rank = rank
    match position:
        case "G":
            p_rank -= replacement_goalie_rank
        case "D":
            p_rank -= replacement_defence_rank
        case "C":
            p_rank -= replacement_centre_rank
        case "C,LW" | "LW":
            p_rank -= replacement_lw_rank
        case _:
            p_rank -= replacement_rw_rank

    return p_rank < keeper_player_rank-replacement_player_rank

def get_team_rank(team):
    print(f'************************************')
    team_rank = 0
    impact_players_involved = 0
    players = []
    for player in team:
        player_rank = get_player_rank(player, print_just_vals)
        team_rank += player_rank
        players.append(PlayerRank(player, player_rank))
        if not player.isdigit() and player_rank >= impact_player_val:
            impact_players_involved += 1

    print(f'')
    print(f'TEAM VALUE - {team_rank}')
    print(f'************************************')

    team = TeamRank(team_rank, players, impact_players_involved)
    return team

def get_player_points(player, season):
    stats = api \
        .league() \
        .players(search=player) \
        .stats(season=season) \
        .get()

    return stats.players[0].points

def get_league(trade_type, trade_count, trade_start):
    league = api \
        .league() \
        .transactions(ttype=trade_type, count=trade_count, start=trade_start) \
        .get()
    return league

def get_pending_trade(trade_type, t_id, trade_count, trade_start):
    league = api \
        .league() \
        .transactions(ttype=trade_type, team_id=t_id, count=trade_count, start=trade_start) \
        .get()
    return league


def get_team(team_id):
    team = api \
        .team(team_id) \
        .roster() \
        .get()
    return team

def get_draft_results():
    draft_results = api \
        .league() \
        .draft_results() \
        .get()
    return draft_results

def get_replacement_rank(position):
    match position:
        case "G":
            return replacement_goalie_rank
        case "D":
            return replacement_defence_rank
        case "C":
            return replacement_centre_rank
        case "C,LW" | "LW":
            return replacement_lw_rank
        case _:
            return replacement_rw_rank 


def get_team_name_by_team_key(key):
    for team in leagueTeams.teams:
        if team.key == key:
            return team.name
    print("***** ERROR: CANNOT MAP TEAM KEY TO TEAM NAME *****")
    return "null"

# if the difference between rank/value of the trade is within 
# trade_difference_level of each other then approve
def get_trade_result(team1_rank, team2_rank, player_max_side):
    rank_difference = team1_rank - team2_rank
    trade_difference_level = inital_trade_difference_level
    player_max_side -= 1
    while player_max_side > 0:
        if player_max_side == 1:
            trade_difference_level += inital_trade_difference_level / 1.5
        else:
            trade_difference_level += inital_trade_difference_level / 2
        player_max_side -= 1
    
    if show_trade_difference_level:
        print(f'TRADE DIFFERENCE LEVEL -- ({trade_difference_level})')

    if rank_difference <= trade_difference_level and rank_difference >= trade_difference_level*-1:
        result = 'RESULT -- TRADE APPROVED'
    elif (rank_difference > 0 and rank_difference - trade_difference_level <= commish_decision_level and rank_difference - trade_difference_level >= commish_decision_level *-1) or \
        (rank_difference < 0 and rank_difference + trade_difference_level <= commish_decision_level and rank_difference + trade_difference_level >= commish_decision_level *-1):
        result = 'RESULT -- COMMISH DECISION'
    else:
        result = 'RESULT -- TRADE REJECTED'
    
    print(result)
    return result