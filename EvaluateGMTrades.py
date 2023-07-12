from yfantasy_api.api import YahooFantasyApi
from TradeAnalyzer import get_league, get_team_rank, get_trade_result, get_team

ttype = "trade" # accepted values "pending_trade" OR "trade"
count = "50" # how many transactions to return in the list
start = "0" # what offset to start the transactions list at

class TeamTradeRating():
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.rating = 0

league = get_league(trade_type=ttype, trade_count=count, trade_start=start)
#league = get_pending_trade(trade_type=ttype, t_id=2, trade_count=count, trade_start=start)

print(f'\n\n\n\n\n\n')

teams = []

for index in range (1, 13):
    team = get_team(team_id=index)
    teams.append(TeamTradeRating(index, team.name))

for transaction in league.transactions:
    team_trader = []
    team_tradee = []

    print(transaction.status)

    if transaction.status == "vetoed":
        continue

    for player in transaction.players_traded:
        if player.source_team_key == transaction.trader_team_key:
            team_trader.append(player.pInfo.name)
        else:
            team_tradee.append(player.pInfo.name)
    
    for pick in transaction.traded_picks:
        if pick.source_team_key == transaction.trader_team_key:
            team_trader.append(pick.round)
        else:
            team_tradee.append(pick.round)
    
    team1 = get_team_rank(team_trader)
    team2 = get_team_rank(team_tradee)

    for team in teams:
        if team.name == transaction.trader_team_name:
            team.rating += team2.rank - team1.rank
        if team.name == transaction.tradee_team_name:
            team.rating += team1.rank - team2.rank

    print(f'\n\n\n\n\n\n')

newTeams = sorted(teams, key=lambda x: x.rating, reverse=True)

count = 1
for team in newTeams:
    print(f'{count}. {team.name} - {team.rating}')
    count += 1