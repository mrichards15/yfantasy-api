from yfantasy_api.api import YahooFantasyApi
from TradeAnalyzer import get_league, get_team_rank, get_trade_result, get_pending_trade

ttype = "trade" # accepted values "pending_trade" OR "trade"
count = "1" # how many transactions to return in the list
start = "0" # what offset to start the transactions list at

league = get_league(trade_type=ttype, trade_count=count, trade_start=start)
#league = get_pending_trade(trade_type=ttype, t_id=2, trade_count=count, trade_start=start)

print(f'\n\n\n\n\n\n')

for transaction in league.transactions:
    team_trader = []
    team_tradee = []

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

    get_trade_result(team1.rank, team2.rank, max(team1.impact_players_num, team2.impact_players_num))

    print(f'\n\n\n\n\n\n')