from yfantasy_api.api import YahooFantasyApi
from TradeAnalyzer import get_league, get_team_rank, get_trade_result

#team1 = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13"]

team1 = ["Juuse Saros", "Igor Shesterkin", "Connor Hellebuyck", "Alexandar Georgiev", "Jake Oettinger", "Linus Ullmark"]
team2 = ["1"]

#team1 = ["Chris Kreider", "Alex Pietrangelo", "10"]
#team2 = ["Jared Spurgeon", "Brock Nelson", "Mark Stone", "6"]

#team1 = ["Timo Meier", "Aaron Ekblad", "Alex Pietrangelo", "12", "13"]
#team2 = ["Drake Batherson", "Dmitry Orlov", "Rickard Rakell", "2", "4"]

#team1 = ["Kirby Dach", "Mathew Barzal", "1", "3"]
#team2 = ["Jack Eichel", "Claude Giroux", "9", "11"]

#team1 = ["Sidney Crosby", "9"]
#team2 = ["Matty Beniers", "4"]

#team1 = [
#"Jack Eichel",
#"Nikita Kucherov",
#"Claude Giroux",
#"Trevor Zegras",
#"Jack Hughes",
#"Drake Batherson",
#"Cole Caufield"
#]

#team2 = ["Connor McDavid"]

######################################################################
# SAMPLE TRADES
######################################################################
#team1 = ["Alexis Lafreniere", "1"]
#team2 = ["Jack Eichel", "9"]

#team1 = ["Robin Lehner", "Sebastian Aho", "Cale Makar"]
#team2 = ["Leon Draisaitl", "Jeremy Swayman", "Linus Ullmark"]

#team1 = ["Andrei Vasilevskiy", "Jaroslav Halak", "12", "13"]
#team2 = ["David Perron", "Kailer Yamamoto", "1", "3"]
######################################################################

print(f'\n\n\n\n\n\n')

team1 = get_team_rank(team1)
team2 = get_team_rank(team2)

get_trade_result(team1.rank, team2.rank, max(team1.impact_players_num, team2.impact_players_num))

print(f'\n\n\n\n\n\n')