from yfantasy_api.api import YahooFantasyApi
from TradeAnalyzer import get_league, get_player_rank, get_player_points
import copy

class TeamRanking:
    def __init__(self, name, rank, pointsRank):
        self.name = name
        self.rank = rank
        self.pointsRank = pointsRank

teams = [["Anaheim Ducks", "Brady Tkachuk", "Mitch Marner", "Quinn Hughes"],
    ["Atlanta Thrashers", "Matthew Tkachuk", "Kirill Kaprizov", "Connor Hellebuyck"],
    ["Boston Bruins", "Nathan MacKinnon", "Jason Robertson", "Brad Marchand"],
    ["Buffalo Sabres", "Cale Makar", "Jake Oettinger", "Tage Thompson"],
    ["Dallas Stars", "Jonathan Huberdeau", "Aleksander Barkov", "Jack Eichel"],
    ["LA Kings", "Leon Draisaitl", "Thatcher Demko", "Shane Wright"],
    ["Montreal Canadiens", "David Pastrnak", "Tim Stutzle", "Ilya Sorokin"],
    ["New York Rangers", "Auston Matthews", "Mikko Rantanen", "Andrei Vasilevskiy"],
    ["Pittsburgh Penguins", "Carter Hart", "William Nylander", "Sidney Crosby"],
    ["Tampa Bay Lightning", "Jack Hughes", "Rasmus Dahlin", "Nikita Kucherov"],
    ["Toronto Maple Leafs", "Connor McDavid", "Igor Shesterkin", "Kyle Connor"],
    ["Washington Capitals", "Elias Pettersson", "Andrei Svechnikov", "Adam Fox"]]

teamsRank = []

for team in teams:
    rank = 0
    pointsRank = 0
    for i in range(1,4):
        p_rank = get_player_rank(team[i], "Nothing")
        if(p_rank < 0):
            p_rank = 0
        rank += p_rank
        pointsRank += get_player_points(team[i], 2022)
        #print(f'{team[i]} - {p_rank}')

    teamsRank.append(TeamRanking(team[0], rank, pointsRank))
    print(f'Hold on still working...just processed {team[0]}')

teamsPointsRank = copy.deepcopy(teamsRank)

print(f'\n\n\n\n\n\n')
print(f'KTFHL KEEPER RANKINGS')
print("--------------------------------------------------")

leagueTeamsCount = 12

while len(teamsRank) > 0:
    numTeams = len(teamsRank)
    index = -1
    highestVal = 0

    for i in range(numTeams):
        if teamsRank[i].rank > highestVal:
            highestVal = teamsRank[i].rank
            index = i
    
    print(f'#{leagueTeamsCount - numTeams + 1} {teamsRank[index].name} - {teamsRank[index].rank}')
    teamsRank.pop(index)


print(f'\n\n\n\n\n\n')

print(f'\n\n\n\n\n\n')
print(f'KTFHL KEEPER POINTS RANKINGS')
print("--------------------------------------------------")

leagueTeamsCount = 12

while len(teamsPointsRank) > 0:
    numTeams = len(teamsPointsRank)
    index = -1
    highestVal = 0

    for i in range(numTeams):
        if teamsPointsRank[i].pointsRank > highestVal:
            highestVal = teamsPointsRank[i].pointsRank
            index = i
    
    print(f'#{leagueTeamsCount - numTeams + 1} {teamsPointsRank[index].name} - {teamsPointsRank[index].pointsRank}')
    teamsPointsRank.pop(index)


print(f'\n\n\n\n\n\n')