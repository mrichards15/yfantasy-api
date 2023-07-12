from yfantasy_api.api import YahooFantasyApi
from TradeAnalyzer import get_league, get_team, get_team_rank, get_player_rank, get_draft_results, get_team_name_by_team_key

class TeamRanking:
    def __init__(self, name, rank):
        self.name = name
        self.rank = rank

account_current_picks = True
account_start_picks_keepers = True

torontoPastKeepersAndPicks = []
atlantaPastKeepersAndPicks = []
bostonPastKeepersAndPicks = []
buffaloPastKeepersAndPicks = []
dallasPastKeepersAndPicks = []
laPastKeepersAndPicks = []
montrealPastKeepersAndPicks = []
newYorkPastKeepersAndPicks = []
pittsburghPastKeepersAndPicks = []
tampaPastKeepersAndPicks = []
washingtonPastKeepersAndPicks = []
anaheimPastKeepersAndPicks = []

#torontoPicks = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13"]
 
torontoPicks =    ["1",  "2",  "3",  "5",  "6",  "8",  "8",  "9",  "11", "11",  "12",  "13",  "13"]
atlantaPicks =    ["2",  "3",  "4",  "5",  "7",  "8",  "9",  "10", "11", "11",  "12",  "12",  "13"]
bostonPicks =     ["1",  "2",  "3",  "4",  "6",  "7",  "7",  "8",  "9",  "10",  "11",  "12",  "13"]
buffaloPicks =    ["1",  "3",  "4",  "5",  "6",  "7",  "8",  "10", "11", "12",  "12",  "13",  "13"]
dallasPicks =     ["1",  "2",  "5",  "6",  "7",  "8",  "8",  "9",  "10", "10",  "11",  "12",  "13"]
laPicks =         ["1",  "1",  "2",  "2",  "3",  "3",  "4",  "5",  "6",  "6",   "7",   "7",   "9"]
montrealPicks =   ["1",  "3",  "4",  "5",  "6",  "8",  "9",  "9",  "10", "11",  "12",  "12",  "13"]
newYorkPicks =    ["1",  "2",  "4",  "5",  "6",  "7",  "8",  "9",  "10", "10",  "11",  "12",  "13"]
pittsburghPicks = ["1",  "2",  "3",  "4",  "4",  "5",  "6",  "6",  "7",  "7",   "8",   "10",  "11"]
tampaPicks =      ["1",  "1",  "2",  "3",  "4",  "5",  "5",  "6",  "7",  "8",   "9",   "11",  "13"]
washingtonPicks = ["2",  "2",  "3",  "3",  "4",  "5",  "9",  "9",  "10", "10",  "11",  "12",  "13"]
anaheimPicks =    ["1",  "2",  "3",  "4",  "4",  "5",  "5",  "6",  "8",  "9",   "10",  "12",  "13"]

league = get_draft_results()
for draft_result in league.draft_results:
    result = ""

    if draft_result.round in range(14, 17):
        result = draft_result.player.name
    else:
        result = str(draft_result.round)

    team_name = get_team_name_by_team_key(draft_result.team_key)

    match team_name:
        case "Toronto Maple Leafs":
            torontoPastKeepersAndPicks.append(result)
        case "Atlanta Thrashers":
            atlantaPastKeepersAndPicks.append(result)
        case "Boston Bruins":
            bostonPastKeepersAndPicks.append(result)
        case "Buffalo Sabres":
            buffaloPastKeepersAndPicks.append(result)
        case "Dallas Stars":
            dallasPastKeepersAndPicks.append(result)
        case "Los Angeles Kings":
            laPastKeepersAndPicks.append(result)
        case "Montreal Canadiens":
            montrealPastKeepersAndPicks.append(result)
        case "New York Rangers":
            newYorkPastKeepersAndPicks.append(result)
        case "Pittsburgh Penguins":
            pittsburghPastKeepersAndPicks.append(result)
        case "Tampa Bay Lightning":
            tampaPastKeepersAndPicks.append(result)
        case "Washington Capitals":
            washingtonPastKeepersAndPicks.append(result)
        case "Anaheim Ducks":
            anaheimPastKeepersAndPicks.append(result)
        case _:
            curPicks = []
            print("***** ERROR GETTING PICKS *****")

teamsRank = []

for index in range (1, 13):
    team = get_team(team_id=index)

    player_ranks = []

    for player in team.players:
        if player.name != "Ryan O'Reilly" and player.name != "K'Andre Miller":
            player_ranks.append(get_player_rank(player.name, "Nothing"))

    team_rank = 0
    count = 0
    player_ranks.sort(reverse=True)

    for rank in player_ranks:
        if count < 16:
            team_rank += rank
            count += 1

    curPicks = []
    pastPicksAndKeepers = []

    match team.name:
        case "Toronto Maple Leafs":
            curPicks = torontoPicks
            pastPicksAndKeepers = torontoPastKeepersAndPicks
        case "Atlanta Thrashers":
            curPicks = atlantaPicks
            pastPicksAndKeepers = atlantaPastKeepersAndPicks
        case "Boston Bruins":
            curPicks = bostonPicks
            pastPicksAndKeepers = bostonPastKeepersAndPicks
        case "Buffalo Sabres":
            curPicks = buffaloPicks
            pastPicksAndKeepers = buffaloPastKeepersAndPicks
        case "Dallas Stars":
            curPicks = dallasPicks
            pastPicksAndKeepers = dallasPastKeepersAndPicks
        case "Los Angeles Kings":
            curPicks = laPicks
            pastPicksAndKeepers = laPastKeepersAndPicks
        case "Montreal Canadiens":
            curPicks = montrealPicks
            pastPicksAndKeepers = montrealPastKeepersAndPicks
        case "New York Rangers":
            curPicks = newYorkPicks
            pastPicksAndKeepers = newYorkPastKeepersAndPicks
        case "Pittsburgh Penguins":
            curPicks = pittsburghPicks
            pastPicksAndKeepers = pittsburghPastKeepersAndPicks
        case "Tampa Bay Lightning":
            curPicks = tampaPicks
            pastPicksAndKeepers = tampaPastKeepersAndPicks
        case "Washington Capitals":
            curPicks = washingtonPicks
            pastPicksAndKeepers = washingtonPastKeepersAndPicks
        case "Anaheim Ducks":
            curPicks = anaheimPicks
            pastPicksAndKeepers = anaheimPastKeepersAndPicks
        case _:
            curPicks = []
            print("***** ERROR GETTING PICKS *****")

    print(f'{team.name} - {team_rank} (No picks)')

    if account_current_picks:
        for pick in curPicks:
            team_rank += get_player_rank(pick, "Nothing")
        print(f'{team.name} - {team_rank} (With current picks)')

    if account_start_picks_keepers:
        for pick in pastPicksAndKeepers:
            team_rank -= get_player_rank(pick, "Nothing")
        print(f'{team.name} - {team_rank} (minus starting picks and keepers)')
    
    teamsRank.append(TeamRanking(team.name, team_rank))
    print(f'Hold on still working...just processed {team.name}')

print(f'\n\n\n\n\n\n')
print(f'KTFHL GM RANKINGS')
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