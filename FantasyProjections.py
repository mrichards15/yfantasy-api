import pandas

df = pandas.read_excel('/Users/Matthew/Documents/GitHub/yfantasy-api/FantasyProjections2223.xls')

#print the column names
#print(df.columns)

#get the values for a given column
#values = df['NAME'].values
values = df['FP'].values

#get a data frame with selected columns
FORMAT = ['NAME', 'AGE', 'FP', 'VORP']
df_selected = df[FORMAT]

def get_player_age(player_name):
    player_age = 26
    try:
        result = df_selected.loc[df['NAME'] == player_name, 'AGE']
        player_age = result.values[0]
    except:
        print(f'****** ERROR GETTING {player_name} AGE ******')
    return player_age

def get_player_projected_points(player_name):
    player_pp = -1
    try:
        result = df_selected.loc[df['NAME'] == player_name, 'FP']
        player_pp = result.values[0]
    except:
        print(f'****** ERROR GETTING {player_name} PROJECTED POINTS ******')
    return player_pp

def get_player_vorp(player_name):
    player_vorp = 0
    try:
        result = df_selected.loc[df['NAME'] == player_name, 'VORP']
        player_vorp = result.values[0]
    except:
        print(f'****** ERROR GETTING {player_name} VORP ******')
    return player_vorp

#print(get_player_age('Connor McDavid'))
#print(get_player_projected_points('Connor McDavid'))
#print(get_player_vorp('Connor McDavid'))