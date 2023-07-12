Stuff to run:

python3 EvaluateCustomTransation.py
python3 EvaluateKeepers.py
python3 EvaluatePowerRankings.py
python3 EvaluateTeamRosters.py
python3 EvluateTransaction.py
python3 FantasyPointsGraph.py
python3 PrintPlayerIdsToCsv.py
python3 EvaluateGMTrades.py
python3 PrintRankingsToCsv.py
python3 EvaluateVorpRanks.py


To update:

......................................................................................................................................
TRADE ANALYZER

Each year league_id must be updated. It is the number at the end of the URL. So in this case https://hockey.fantasysports.yahoo.com/hockey/610 the league_id is 610.

You will also need to update the player projections. This is gotten from Dom's rankings and inputting the leagues stats. Copy that over to a new excel sheet with the following headings NAME AGE FP VORP and name the file FantasyProjections2x2x.xls. Change the projection files it's pointing to but going to FantasyProjections.py and changing the file it points to

Another thing that needs updated is potentially the replacement ranks and draft picks. You can run EvaluateVorpRanks.py to find out what these should be. Remember to include new players in PrintRankingsToCsv.py

......................................................................................................................................


......................................................................................................................................
DRAFT

Go to https://www.hockeydb.com/ihdb/draft/nhl2022e.html copy and paste draft from that year
......................................................................................................................................

......................................................................................................................................
SEASON STATS

Go to https://www.hockey-reference.com/leagues/NHL_2023_skaters.html

Hockey-Reference > Seasons > Summary > Skaters > Basic Stats > Sort by points header > Get as Excel Workbook > Paste results into new table in nhl-stats.xls

Hockey-Reference > Seasons > Summary > Goalies > Get as Excel Workbook > Paste results into same table below in nhl-stats.xls
......................................................................................................................................

......................................................................................................................................
PLAYER API IDs

Either run https://suggest.svc.nhl.com/svc/suggest/v1/minplayers/John%20Gibson/10 to get an individual player and insert into nhl-stats.xls or for many run python3 PrintPlayerIdsToCsv.py
......................................................................................................................................

......................................................................................................................................
FANTASY PROJECTIONS
Paste new Xls with fantasy projections (needs to have NAME AGE FP VORP as columns)

In FantasyProjections.py change the file that is read
......................................................................................................................................

