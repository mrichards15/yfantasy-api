from flask import Flask
from flask import request
from flask import render_template
from yfantasy_api.api.api import YahooFantasyApi

from TradeAnalyzer import get_league, get_team_rank, get_trade_result

league_id = 610  # This should be the id of the league you are querying
game_id = 'nhl'    # This should be the id of the game you are querying
team_id = 1        # This should be the id of the team you are querying

api = YahooFantasyApi(league_id, game_id)

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template("my-form.html") # This should be the name of your HTML file

@app.route('/', methods=['POST'])
def my_form_post():
    team1 = request.form['team1']
    team2 = request.form['team2']

    team1Result = []
    for p in team1.split('\n'):
        team1Result.append(p.replace("\r", ""))

    team2Result = []
    for p in team2.split('\n'):
        team2Result.append(p.replace("\r", ""))

    team1Rank = get_team_rank( team1Result )
    team2Rank = get_team_rank( team2Result )

    tradeResult = get_trade_result(team1Rank.rank, team2Rank.rank, max(team1Rank.impact_players_num, team2Rank.impact_players_num))

    resultPage = "<h1>" + tradeResult + "</h1><div><br><br>"

    resultPage += "<p>************************************************************************</p>"

    for player in team1Rank.players:
        if player.name.isnumeric():
            resultPage += "<p>DRAFT PICK ROUND " + player.name + " VALUE -- " + str(player.rank) + "</p>"
        else:
            resultPage += "<p>" + player.name + " VALUE -- " + str(player.rank) + "</p>"
    
    resultPage += "<b>TEAM VALUE -- " + str(team1Rank.rank) + "</b></div>"

    resultPage += "<p>************************************************************************</p>"
    resultPage += "<p>************************************************************************</p>"

    for player in team2Rank.players:
        if player.name.isnumeric():
            resultPage += "<p>DRAFT PICK ROUND " + player.name + " VALUE -- " + str(player.rank) + "</p>"
        else:
            resultPage += "<p>" + player.name + " VALUE -- " + str(player.rank) + "</p>"
    
    resultPage += "<b>TEAM VALUE -- " + str(team2Rank.rank) + "</b></div>"

    resultPage += "<p>************************************************************************</p>"

    return resultPage

if __name__ == '__main__':
    app.run()