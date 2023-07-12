pick_value_round_1 = 331
pick_value_round_2 = 314
pick_value_round_3 = 303
pick_value_round_4 = 290
pick_value_round_5 = 283
pick_value_round_6 = 275
pick_value_round_7 = 270
pick_value_round_8 = 262
pick_value_round_9 = 255
pick_value_round_10 = 250
pick_value_round_11 = 245
pick_value_round_12 = 241
pick_value_round_13 = 235

#2021-22
#pick_value_round_1 = 350
#pick_value_round_2 = 333
#pick_value_round_3 = 315
#pick_value_round_4 = 305
#pick_value_round_5 = 293
#pick_value_round_6 = 282
#pick_value_round_7 = 276
#pick_value_round_8 = 266
#pick_value_round_9 = 260
#pick_value_round_10 = 252
#pick_value_round_11 = 245
#pick_value_round_12 = 237
#pick_value_round_13 = 230

#2020-21
#pick_value_round_1 = 324
#pick_value_round_2 = 310
#pick_value_round_3 = 299    
#pick_value_round_4 = 286
#pick_value_round_5 = 280
#pick_value_round_6 = 273
#pick_value_round_7 = 268
#pick_value_round_8 = 261
#pick_value_round_9 = 254
#pick_value_round_10 = 252
#pick_value_round_11 = 250
#pick_value_round_12 = 243
#pick_value_round_13 = 237

def get_draft_pick_value(draft_pick):
    match draft_pick:
        case "1":
            return pick_value_round_1
        case "2":
            return pick_value_round_2
        case "3":
            return pick_value_round_3
        case "4":
            return pick_value_round_4
        case "5":
            return pick_value_round_5
        case "6":
            return pick_value_round_6
        case "7":
            return pick_value_round_7
        case "8":
            return pick_value_round_8
        case "9":
            return pick_value_round_9
        case "10":
            return pick_value_round_10
        case "11":
            return pick_value_round_11
        case "12":
            return pick_value_round_12
        case "13":
            return pick_value_round_13
        case _:
            return 0