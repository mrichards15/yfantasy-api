from yfantasy_api.api import YahooFantasyApi
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf as bplt

league_id = 874  # This should be the id of the league you are querying
game_id = 'nhl'    # This should be the id of the game you are querying
team_id = 1        # This should be the id of the team you are querying

plot_wins = True
plot_points = True

api = YahooFantasyApi(league_id, game_id)

league = api \
    .league() \
    .get()

startWeek = league.start_week
curWeek = league.current_week

leagueTeams = api \
    .league() \
    .teams() \
    .get()

teamsStats = []

class TeamStats:
    def __init__(self, key, name):
        self.key = key
        self.name = name
        self.week_wins = [0]
        self.week_points = [0]
        self.total_points = [0]

for team in leagueTeams.teams:
    teamsStats.append(TeamStats(team.key, team.name))

def add_win_to_team(team):
    for teamStats in teamsStats:
        if team.key == teamStats.key:
            win_count = teamStats.week_wins[-1] + 1
            teamStats.week_wins.append(win_count)

def add_loss_to_team(team):
    for teamStats in teamsStats:
        if team.key == teamStats.key:
            win_count = teamStats.week_wins[-1]
            teamStats.week_wins.append(win_count)

def add_team_points(team):
    for teamStats in teamsStats:
        if team.key == teamStats.key:
            points_total = teamStats.total_points[-1] + team.points
            teamStats.total_points.append(points_total)
            teamStats.week_points.append(team.points)

weeks = [0]

if plot_wins:
    for weekNum in range(startWeek, curWeek):
        print("Processing wins...")
        weeks.append(weekNum)

        scoreboard = api \
            .league() \
            .scoreboard(week=weekNum) \
            .get()

        for matchup in scoreboard.matchups:
            add_win_to_team(matchup.winning_team)
            add_loss_to_team(matchup.losing_team)

if plot_points:
    for leagueTeam in leagueTeams.teams:
        print("Processing points...")
        points = 0

        for week in range(startWeek, curWeek):
            team = api \
                .team(team_id=leagueTeam.id) \
                .stats(week=week) \
                .get()

            add_team_points(team)


pdf = bplt.PdfPages("SeasonStandings.pdf")

fig1 = plt.figure()
for teamStats in teamsStats:
    print(f'{teamStats.name}, {teamStats.week_wins}')
    plt.plot(weeks, teamStats.week_wins, label=teamStats.name)
plt.xlabel('Week')
plt.ylabel('Wins')
plt.title('Standings for Season')
plt.legend(fontsize=4)
pdf.savefig(fig1)

fig2 = plt.figure()
for teamStats in teamsStats:
    print(f'{teamStats.name}, {teamStats.total_points}')
    plt.plot(weeks, teamStats.total_points, label=teamStats.name)
plt.xlabel('Week')
plt.ylabel('Points')
plt.title('Points for Season')
plt.legend(fontsize=4)
pdf.savefig(fig2)

pdf.close()

