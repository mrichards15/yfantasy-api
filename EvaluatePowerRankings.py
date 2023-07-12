from yfantasy_api.api import YahooFantasyApi
from FantasyProjections import get_player_age, get_player_projected_points
from DraftPickValues import get_draft_pick_value
from yfantasy_api.models import transaction

league_id = 610  # This should be the id of the league you are querying
game_id = 'nhl'    # This should be the id of the game you are querying
team_id = 1        # This should be the id of the team you are querying

start_week = 1 # start week to query
end_week = 10 # end week to query

api = YahooFantasyApi(league_id, game_id)

class TeamRanking:
    def __init__(self, name, points):
        self.name = name
        self.points = points

leagueTeams = api \
    .league() \
    .teams() \
    .get()

teamRankings = []

for leagueTeam in leagueTeams.teams:
    points = 0

    for week in range(start_week, end_week+1):
        team = api \
            .team(team_id=leagueTeam.id) \
            .stats(week=week) \
            .get()

        points += team.points
    
    teamRankings.append(TeamRanking(team.name, points))
    print(f'Hold on still working...just processed {team.name}')


print("")
print("")
print("")
print("")
print("")
print(f'KTFHL POWER RANKINGS FOR WEEKS {start_week}-{end_week}')
print("--------------------------------------------------")

leagueTeamsCount = len(leagueTeams.teams)

while len(teamRankings) > 0:
    numTeams = len(teamRankings)
    index = -1
    highestVal = 0

    for i in range(numTeams):
        if teamRankings[i].points > highestVal:
            highestVal = teamRankings[i].points
            index = i
    
    print(f'#{leagueTeamsCount - numTeams + 1} {teamRankings[index].name} - {teamRankings[index].points}')
    teamRankings.pop(index)