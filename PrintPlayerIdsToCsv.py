import requests
import json
import csv


team = [
"Jonas Siegenthaler",
"Miles Wood",
"Jonatan Berggren",
"Noah Cates",
"Juuso Parssinen",
"John-Jason Peterka",
"Noel Acciari",
"Connor Clifton",
"Alexander Romanov",
"Jake Muzzin",
"Arber Xhekaj"
]

outfile = open('./rankings/PlayerIds3.csv','w')
writer=csv.writer(outfile)
writer.writerow(['Player', 'Id'])

player_name = ""
player_age = 18
player_team = ""
player_num_results = ""

for player in team:
    try:
        response = requests.get("https://suggest.svc.nhl.com/svc/suggest/v1/minplayers/" + player + "/3")
        json_result = json.loads(response.text)
        player_data = json_result["suggestions"][0]
        player_id = player_data.split('|')[0]
        playerRow = [player, player_id]
        writer.writerow(playerRow)
        print(f'{player} - {player_id} just processed')
    except:
        playerRow = [player, "NOT FOUND"]
        writer.writerow(playerRow)
        print(f'****** ERROR GETTING {player} ******')
    

#response = requests.get("https://suggest.svc.nhl.com/svc/suggest/v1/minplayers/" + player_name + "/3")
#json_result = json.loads(response.text)
#player_data = json_result["suggestions"][0]
#player_id = player_data.split('|')[0]

#response = requests.get("https://statsapi.web.nhl.com/api/v1/people/" + player_id + "/stats?stats=statsSingleSeason&season=20222023")



#test = '{ "copyright" : "NHL and the NHL Shield are registered trademarks of the National Hockey League. NHL and NHL team marks are the property of the NHL and its teams. © NHL 2022. All Rights Reserved.",  "stats" : [ {    "type" : {      "displayName" : "statsSingleSeason",      "gameType" : {        "id" : "R",        "description" : "Regular season",        "postseason" : false      }    },    "splits" : [ {      "season" : "20222023",      "stat" : {        "timeOnIce" : "266:16",        "assists" : 13,        "goals" : 12,        "pim" : 4,        "shots" : 47,        "games" : 12,        "hits" : 12,        "powerPlayGoals" : 6,        "powerPlayPoints" : 12,        "powerPlayTimeOnIce" : "55:14",        "evenTimeOnIce" : "204:35",        "penaltyMinutes" : "4",        "faceOffPct" : 55.73,        "shotPct" : 25.5,        "gameWinningGoals" : 2,        "overTimeGoals" : 0,        "shortHandedGoals" : 0,        "shortHandedPoints" : 0      }    } ]  } ]}'
#json_result = json.loads(response.text)
#print(json_result["stats"][0]["splits"][0]["stat"]["games"])