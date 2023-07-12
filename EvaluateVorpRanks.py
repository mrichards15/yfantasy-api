from yfantasy_api.api import YahooFantasyApi
from PrintRankingsToCsv import PrintRankings
import csv
import pandas

# NEED TO COMMENT OUT LAST LINE IN PrintRankingsToCsv!!!!!!!!!!!!!!!

class PlayerCsv:
    def __init__(self, Player, Position, PreVorp, RichVal):
        self.Player = Player
        self.Position = Position
        self.PreVorp = PreVorp
        self.RichVal = RichVal

class PositionVorp:
    def __init__(self, PreVorp, RichVal):
        self.PreVorp = PreVorp
        self.RichVal = RichVal

def FindReplacementRank(rankings, upToCount, possiblePositionsArr):
    counter = 1
    offset = False
    for player in rankings:
        if counter == upToCount:
            return PositionVorp(player.PreVorp, player.RichVal)
        if player.Position in possiblePositionsArr:
            if offset:
                offset = False
            else:
                offset = True
                counter += 1
        else:
            counter += 1

replacement_forward_rank = PositionVorp(0, 0) # rank of the 108th ranked F
replacement_centre_rank = PositionVorp(0, 0) # rank of the 36th ranked C
replacement_lw_rank = PositionVorp(0, 0) # rank of the 36th ranked LW
replacement_rw_rank = PositionVorp(0, 0) # rank of a 36th ranked RW
replacement_defence_rank = PositionVorp(0, 0) # rank of a 48th ranked D
replacement_goalie_rank = PositionVorp(0, 0) # rank of a 30th ranked G
replacement_player_rank = PositionVorp(0, 0) # rank of 192th ranked player
keeper_cutoff_rank = PositionVorp(0, 0) # rank of 36th ranked player

#fileName = PrintRankings()
fileName = './rankings/PlayersRichValRankings-2023-01-20-45.csv'

print(f'\n\n\n\n\n\n')
print('****************************************************************************************************')
print('')
print('VALUES BY VORP')
print('')
print('****************************************************************************************************')
print('')
df = pandas.read_csv(fileName)

playerRankings = [(PlayerCsv(row.Player,row.Position,row.PreVORP,row.RichVal)) for index, row in df.iterrows() ] 

playerPreVorpRankings = sorted(playerRankings, key=lambda x: x.PreVorp, reverse=True)
playerRichValRankings = sorted(playerRankings, key=lambda x: x.RichVal, reverse=True)

forwardRankings = sorted(filter(lambda x: x.Position in ['C', 'LW', 'RW', 'C,LW', 'C,RW', 'LW,RW', 'C,LW,RW'], playerRankings), key=lambda x: x.PreVorp, reverse=True)
centreRankings = sorted(filter(lambda x: x.Position in ['C', 'C,LW', 'C,RW', 'C,LW,RW'], playerRankings), key=lambda x: x.PreVorp, reverse=True)
lwRankings = sorted(filter(lambda x: x.Position in ['LW', 'C,LW', 'LW,RW', 'C,LW,RW'], playerRankings), key=lambda x: x.PreVorp, reverse=True)
rwRankings = sorted(filter(lambda x: x.Position in ['RW', 'C,RW', 'LW,RW', 'C,LW,RW'], playerRankings), key=lambda x: x.PreVorp, reverse=True)
defenceRankings = sorted(filter(lambda x: x.Position == 'D', playerRankings), key=lambda x: x.PreVorp, reverse=True)
goalieRankings = sorted(filter(lambda x: x.Position == 'G', playerRankings), key=lambda x: x.PreVorp, reverse=True)

replacement_centre_rank = FindReplacementRank(centreRankings, 36, ['C,LW', 'C,RW', 'C,LW,RW'])
replacement_lw_rank = FindReplacementRank(lwRankings, 36, ['C,LW', 'LW,RW', 'C,LW,RW'])
replacement_rw_rank = FindReplacementRank(rwRankings, 36, ['C,RW', 'LW,RW', 'C,LW,RW'])
replacement_forward_rank = PositionVorp(forwardRankings[107].PreVorp, forwardRankings[107].RichVal)
replacement_defence_rank = PositionVorp(defenceRankings[47].PreVorp, defenceRankings[47].RichVal)
replacement_goalie_rank = PositionVorp(goalieRankings[29].PreVorp, goalieRankings[29].RichVal)
replacement_player_rank = PositionVorp(playerPreVorpRankings[192].PreVorp, playerPreVorpRankings[192].RichVal)
keeper_cutoff_rank = PositionVorp(playerPreVorpRankings[35].PreVorp, playerPreVorpRankings[35].RichVal)

forwardRichValRankings = sorted(filter(lambda x: x.Position in ['C', 'LW', 'RW', 'C,LW', 'C,RW', 'LW,RW', 'C,LW,RW'], playerRankings), key=lambda x: x.RichVal, reverse=True)
centreRichValRankings = sorted(filter(lambda x: x.Position in ['C', 'C,LW', 'C,RW', 'C,LW,RW'], playerRankings), key=lambda x: x.RichVal, reverse=True)
lwRichValRankings = sorted(filter(lambda x: x.Position in ['LW', 'C,LW', 'LW,RW', 'C,LW,RW'], playerRankings), key=lambda x: x.RichVal, reverse=True)
rwRichValRankings = sorted(filter(lambda x: x.Position in ['RW', 'C,RW', 'LW,RW', 'C,LW,RW'], playerRankings), key=lambda x: x.RichVal, reverse=True)
defenceRichValRankings = sorted(filter(lambda x: x.Position == 'D', playerRankings), key=lambda x: x.RichVal, reverse=True)
goalieRichValRankings = sorted(filter(lambda x: x.Position == 'G', playerRankings), key=lambda x: x.RichVal, reverse=True)

replacement_centre_richval = FindReplacementRank(centreRichValRankings, 36, ['C,LW', 'C,RW', 'C,LW,RW']).RichVal
replacement_lw_richval = FindReplacementRank(lwRichValRankings, 36, ['C,LW', 'LW,RW', 'C,LW,RW']).RichVal
replacement_rw_richval = FindReplacementRank(rwRichValRankings, 36, ['C,RW', 'LW,RW', 'C,LW,RW']).RichVal
replacement_forward_richval = forwardRichValRankings[107].RichVal
replacement_defence_richval = defenceRichValRankings[47].RichVal
replacement_goalie_richval = goalieRichValRankings[29].RichVal
replacement_player_richval = playerRichValRankings[192].RichVal
keeper_cutoff_richval = playerRichValRankings[35].RichVal

print(f'Replacement F Rank: by VORP {replacement_forward_rank.PreVorp}, by RichVal {replacement_forward_rank.RichVal}')
print(f'Replacement C Rank: by VORP {replacement_centre_rank.PreVorp}, by RichVal {replacement_centre_rank.RichVal}')
print(f'Replacement LW Rank: by VORP {replacement_lw_rank.PreVorp}, by RichVal {replacement_lw_rank.RichVal}')
print(f'Replacement RW Rank: by VORP {replacement_rw_rank.PreVorp}, by RichVal {replacement_rw_rank.RichVal}')
print(f'Replacement D Rank: by VORP {replacement_defence_rank.PreVorp}, by RichVal {replacement_defence_rank.RichVal}')
print(f'Replacement G Rank: by VORP {replacement_goalie_rank.PreVorp}, by RichVal {replacement_goalie_rank.RichVal}')
print(f'Replacement Player Rank: by VORP {replacement_player_rank.PreVorp}, by RichVal {replacement_player_rank.RichVal}')
print('')
print(f'Keeper Cutoff Rank: by VORP {keeper_cutoff_rank.PreVorp} = {keeper_cutoff_rank.PreVorp - replacement_player_rank.PreVorp} RichVal')
print('')
print('Draft Picks Rank by VORP')
print(f'1st Round: by VORP {playerPreVorpRankings[41].PreVorp} = {playerPreVorpRankings[41].PreVorp - replacement_player_rank.PreVorp} RichVal')
print(f'2nd Round: by VORP {playerPreVorpRankings[53].PreVorp} = {playerPreVorpRankings[53].PreVorp - replacement_player_rank.PreVorp} RichVal')
print(f'3rd Round: by VORP {playerPreVorpRankings[65].PreVorp} = {playerPreVorpRankings[65].PreVorp - replacement_player_rank.PreVorp} RichVal')
print(f'4th Round: by VORP {playerPreVorpRankings[77].PreVorp} = {playerPreVorpRankings[77].PreVorp - replacement_player_rank.PreVorp} RichVal')
print(f'5th Round: by VORP {playerPreVorpRankings[89].PreVorp} = {playerPreVorpRankings[89].PreVorp - replacement_player_rank.PreVorp} RichVal')
print(f'6th Round: by VORP {playerPreVorpRankings[101].PreVorp} = {playerPreVorpRankings[101].PreVorp - replacement_player_rank.PreVorp} RichVal')
print(f'7th Round: by VORP {playerPreVorpRankings[113].PreVorp} = {playerPreVorpRankings[113].PreVorp - replacement_player_rank.PreVorp} RichVal')
print(f'8th Round: by VORP {playerPreVorpRankings[125].PreVorp} = {playerPreVorpRankings[125].PreVorp - replacement_player_rank.PreVorp} RichVal')
print(f'9th Round: by VORP {playerPreVorpRankings[137].PreVorp} = {playerPreVorpRankings[137].PreVorp - replacement_player_rank.PreVorp} RichVal')
print(f'10th Round: by VORP {playerPreVorpRankings[149].PreVorp} = {playerPreVorpRankings[149].PreVorp - replacement_player_rank.PreVorp} RichVal')
print(f'11th Round: by VORP {playerPreVorpRankings[161].PreVorp} = {playerPreVorpRankings[161].PreVorp - replacement_player_rank.PreVorp} RichVal')
print(f'12th Round: by VORP {playerPreVorpRankings[173].PreVorp} = {playerPreVorpRankings[173].PreVorp - replacement_player_rank.PreVorp} RichVal')
print(f'13th Round: by VORP {playerPreVorpRankings[185].PreVorp} = {playerPreVorpRankings[185].PreVorp - replacement_player_rank.PreVorp} RichVal')
print('')
print('****************************************************************************************************')
print('')
print('VALUES BY RICHVAL')
print('')
print('****************************************************************************************************')
print('')
print(f'Replacement F Rank by RichVal: {replacement_forward_richval}')
print(f'Replacement C Rank by RichVal: {replacement_centre_richval}')
print(f'Replacement LW Rank by RichVal: {replacement_lw_richval}')
print(f'Replacement RW Rank by RichVal: {replacement_rw_richval}')
print(f'Replacement D Rank by RichVal: {replacement_defence_richval}')
print(f'Replacement G Rank by RichVal: {replacement_goalie_richval}')
print(f'Replacement Player Rank by RichVal: {replacement_player_richval}')
print('')
print(f'Keeper Cutoff Rank by RichVal: {keeper_cutoff_richval}')
print('')
print('Draft Picks Rank by RichVal')
print(f'1st Round: by RichVal {playerRichValRankings[41].RichVal}')
print(f'2nd Round: by RichVal {playerRichValRankings[53].RichVal}')
print(f'3rd Round: by RichVal {playerRichValRankings[65].RichVal}')
print(f'4th Round: by RichVal {playerRichValRankings[77].RichVal}')
print(f'5th Round: by RichVal {playerRichValRankings[89].RichVal}')
print(f'6th Round: by RichVal {playerRichValRankings[101].RichVal}')
print(f'7th Round: by RichVal {playerRichValRankings[113].RichVal}')
print(f'8th Round: by RichVal {playerRichValRankings[125].RichVal}')
print(f'9th Round: by RichVal {playerRichValRankings[137].RichVal}')
print(f'10th Round: by RichVal {playerRichValRankings[149].RichVal}')
print(f'11th Round: by RichVal {playerRichValRankings[161].RichVal}')
print(f'12th Round: by RichVal {playerRichValRankings[173].RichVal}')
print(f'13th Round: by RichVal {playerRichValRankings[185].RichVal}')
print('')
print('****************************************************************************************************')
print(f'\n\n\n\n\n\n')

