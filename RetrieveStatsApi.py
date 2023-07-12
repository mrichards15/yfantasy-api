from NHLStats import get_player_id_csv, get_team_id_csv
import requests
import json

class PlayerStats:
    def __init__(self, name, gp, goals, assists, plusMinus, pim, powerPlayPoints, shortHandedPoints, gameWinningGoals, shots, blocked):
        self.name = name
        self.gp = gp
        self.goals = goals
        self.assists = assists
        self.plusMinus = plusMinus
        self.pim = pim
        self.powerPlayPoints = powerPlayPoints
        self.shortHandedPoints = shortHandedPoints
        self.gameWinningGoals = gameWinningGoals
        self.shots = shots
        self.blocked = blocked

    def get_fantasy_points(self):
        return self.goals * 3 + self.assists * 2 + self.plusMinus * 1 + self.pim * 0.3 + \
            self.powerPlayPoints * 1 + self.shortHandedPoints * 2 + self.gameWinningGoals * 3 + \
            self.shots * 0.4 + self.blocked * 0.4

class GoalieStats:
    def __init__(self, name, gp, wins, goalsAgainst, saves, shutouts):
        self.name = name
        self.gp = gp
        self.wins = wins
        self.goalsAgainst = goalsAgainst
        self.saves = saves
        self.shutouts = shutouts
    
    def get_fantasy_points(self):
        return self.wins * 4 + self.goalsAgainst * -1 + self.saves * 0.2 + self.shutouts * 2

# see https://gitlab.com/dword4/nhlapi/-/blob/master/stats-api.md#people for API documentation

def get_player_stats_api(player_name, is_goalie, season):
    player_api_id = get_player_id_csv(player_name)
    season_api = str(season) + str(season+1)
    player_gp = -1
    
    try:
        response = requests.get("https://statsapi.web.nhl.com/api/v1/people/" + str(player_api_id) + "/stats?stats=statsSingleSeason&season=" + str(season_api))
        json_result = json.loads(response.text)
        result = json_result["stats"][0]["splits"][0]["stat"]
        player_gp = result["games"]

        if is_goalie:
            wins = result["wins"]
            goalsAgainst = result["goalsAgainst"]
            saves = result["saves"]
            shutouts = result["shutouts"]

            return GoalieStats(player_name, player_gp, wins, goalsAgainst, saves, shutouts)
        else:
            goals = result["goals"]
            assists = result["assists"]
            plusMinus = result["plusMinus"]
            pim = result["pim"]
            powerPlayPoints = result["powerPlayPoints"]
            shortHandedPoints = result["shortHandedPoints"]
            gameWinningGoals = result["gameWinningGoals"]
            shots = result["shots"]
            blocked = result["blocked"]

            return PlayerStats(player_name, player_gp, goals, assists, plusMinus, pim, \
                powerPlayPoints, shortHandedPoints, gameWinningGoals, shots, blocked)
        
    except:
        print(f'****** ERROR GETTING {player_name} GP in SEASON {season} from API ******')

    return PlayerStats(player_name, player_gp, 0, 0, 0, 0, 0, 0, 0, 0, 0)

def get_team_gp_api(team_name):
    team_api_id = get_team_id_csv(team_name)
    team_gp = -1
    
    try:
        response = requests.get("https://statsapi.web.nhl.com/api/v1/teams/" + str(team_api_id) + "?expand=team.stats")
        json_result = json.loads(response.text)
        team_gp = json_result["teams"][0]["teamStats"][0]["splits"][0]["stat"]["gamesPlayed"]
    except:
        print(f'****** ERROR GETTING {team_name} GP from API ******')
    return team_gp

      
#print(get_player_gp_api("Auston Matthews", False, 2022).get_fantasy_points())
#print(get_player_gp_api("Kirby Dach", 2022))
#print(get_team_gp_api("TOR"))