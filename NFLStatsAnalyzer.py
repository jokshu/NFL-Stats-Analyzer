import NFLStatsDatabase as NFL
import math

Options = ["week", "reg", "post", "reg+post"]
x = 0
Equations = {
    "WR_Prod_Gauss": 1.25 * math.e ** -0.0145 * (x - 27.5)**2,
    "RB_Prod_Gauss": 1.2 * math.e ** -0.0175 * (x - 25)**2,
    "TE_Prod_Gauss": (math.e ** -0.0175 * (x - 28.5) ** 2) + (0.35 * math.e ** -1 * (x - 26) ** 2) + (0.255 * math.e ** -1 * (x - 29) ** 2),
    "QB_Prod_Gauss": (0.85 * math.e ** -0.025 * (x - 30) ** 2) + (0.2 * math.e ** -1.5 * (x - 26) ** 2) + (0.4 * math.e ** -0.5 * (x - 30) ** 2) - (0.075 * math.e ** -1 * (x - 33) ** 2)
    }

def align(list, columnwidth): #aligns the inputed text to match a table format with (columnwidth) spaces between each column
    resp = ""
    for word in list:
        resp += str(word) + " " * (columnwidth - len(str(word)))
    return resp

def Create_Database(Filter, Seasons):
    if Seasons == True:
        Seasons = [1999, 2026]
    elif type(Seasons) == int:
        Seasons = [Seasons, Seasons]
        
    Positions = NFL.Load_Database(-1, [Seasons[0], Seasons[0]], Options[-1], Filter)
    
    i = 1
    while i + Seasons[0] <= Seasons[-1]: #Loop thru seasons and add up player stats during them
        Position = NFL.Load_Database(-1, [Seasons[0] + i, Seasons[0] + i], Options[-1], Filter)
        for key, val in Position.items():
            if key in Positions:
                for kkey, kval in val.items():
                    if kkey != "ID" and kkey != "Name" and kkey != "Birthdate" and kkey != "Age" and kkey != "Position" and kkey != "Position Group" and kkey != "Headshot":
                        Positions[key][kkey] += kval
            else:
                Positions[key] = val
        i += 1
    return Positions

def Create_Leaderboard(Index, Database, Amount, PreSpace=5, ColumnSpacing=17):
    i = 1
    SortedPoints = sorted(Database.items(), key=lambda kv: kv[1])
    PreSpace = 5
    ColumnSpacing = 17
    
    print(align(["No.", align(["Name", Index], ColumnSpacing)], PreSpace))
    while i <= min(len(SortedPoints), Amount):
        ID, Points = SortedPoints[-1*i]
        Name = Players[ID]["Name"]
        print(align([i, align([Name, str(Points)], ColumnSpacing)], PreSpace))
        i += 1

def Fantasy_Points(Players, Amount):
    Database = dict()
    
    for key, Player in Players.items():
        ID = Player["ID"]
        Total_Yards = Player["Total Yards"]
        Total_Touchdowns = Player["Total Touchdowns"]
        Fumbles = Player["Fumbles"]
        Targets = Player["Targets"]
        Receptions = Player["Receptions"]
        
        Passing_Touchdowns = Player["Passing Touchdowns"]
        Passing_Yards = Player["Passing Yards"]
        Attempts = Player["Attempts"]
        Completions = Player["Completions"]
        Sacks_Taken = Player["Sacks Taken"]
        Interceptions_Thrown = Player["Passing Interceptions"]
        
        Yard_Points = (0.1 * (Total_Yards - Passing_Yards)) + (0.04 * Passing_Yards)
        Touchdown_Points = (6 * (Total_Touchdowns - Passing_Touchdowns)) + (6 * Passing_Touchdowns)
        Fumble_Points = (-2 * (Fumbles)) + (-2 * (Interceptions_Thrown))
        Reception_Points = (0.5 * (Receptions)) + (0.02 * Completions)
        Missed_Target_Points = (-0.1 * (Targets - Receptions)) + (-0.04 * (Attempts - Completions)) + (-0.04 * Sacks_Taken)
        
        Total_Points = round(Yard_Points + Touchdown_Points + Fumble_Points + Reception_Points + Missed_Target_Points, 2)
        Database[ID] = Total_Points
        
    Create_Leaderboard("Fantasy Points", Database, Amount)

def Breakout_Index(Players, Amount):
    Database = dict()
    
    for key, Player in Players.items():
        ID = Player["ID"]
        Position = Player["Position"]
        Age = Player["Age"]
        x = Age
        if Age == 0:
            API = 1
            
        API = Equations[f"{Position}_Prod_Gauss"] #Age_Production_Index
        
        Total_Yards = Player["Total Yards"]
        Total_Tds = Player["Total Touchdowns"]
        Fumbs = Player["Fumbles"]
        
        Carrs = Player["Carries"]
        Rush_Yards = max(Player["Rushing Yards"], 0)
        
        Rec_Yards = max(Player["Receiving Yards"], 0)
        YAC = max(Player["Receiving Yards After Catch"], 0)
        Targets = Player["Targets"]
        Rec = Player["Receptions"]
        Air_Yards = YAC - Rec_Yards
        
        Passing_Tds = Player["Passing Touchdowns"]
        Passing_Yards = Player["Passing Yards"]
        Atts = Player["Attempts"]
        Comps = Player["Completions"]
        Sacks_Taken = Player["Sacks Taken"]
        Interceptions_Thrown = Player["Passing Interceptions"]
        
        Yard_Points = (0.1 * (Total_Yards - Passing_Yards)) + (0.02 * Passing_Yards)
        Touchdown_Points = (6 * (Total_Tds - Passing_Tds)) + (6 * Passing_Tds)
        Fumble_Points = (-2 * (Fumbs)) + (-2 * (Interceptions_Thrown))
        Reception_Points = (0.1 * (Rec)) + (0.02 * Comps) + (0.05 * Carrs)
        Missed_Target_Points = (-0.025 * (Targets - Rec)) + (-0.01 * (Atts - Comps)) + (-0.02 * Sacks_Taken)
        
        Total_Points = round((Yard_Points + Touchdown_Points + Fumble_Points + Reception_Points + Missed_Target_Points) * (API/10000), 1)
        Database[ID] = Total_Points

    Create_Leaderboard("Breakout Score", Database, Amount)

def Relative_Prime_Index(Players, Amount):
    Database = dict()
    
    for key, Player in Players.items():
        ID = Player["ID"]
        Position = Player["Position"]
        Age = Player["Age"]
        x = Age
        API = Equations[f"{Position}_Prod_Gauss"] #Age_Production_Index
        if Age == 0:
            API = 1
        
        Total_Yards = Player["Total Yards"]
        Total_Tds = Player["Total Touchdowns"]
        Fumbs = Player["Fumbles"]
        
        Car = Player["Carries"]
        Rush_Yards = max(Player["Rushing Yards"], 0)
        
        Rec_Yards = max(Player["Receiving Yards"], 0)
        YAC = max(Player["Receiving Yards After Catch"], 0)
        Targets = Player["Targets"]
        Rec = Player["Receptions"]
        Air_Yards = YAC - Rec_Yards
        
        Passing_Tds = Player["Passing Touchdowns"]
        Passing_Yards = Player["Passing Yards"]
        Atts = Player["Attempts"]
        Comps = Player["Completions"]
        Sacks_Taken = Player["Sacks Taken"]
        Interceptions_Thrown = Player["Passing Interceptions"]
        
#        Yard_Points = (0.1 * (Total_Yards - Passing_Yards)) + (0.04 * Passing_Yards)
        Touchdown_Points = 3 * ((Total_Tds - Passing_Tds)/(Car + Rec + 1)) + (3 * ((Passing_Tds)/(Comps + 1)))
#        Fumble_Points = (-2 * (Fumbs)) + (-2 * (Interceptions_Thrown))
        Reception_Points = (0.5 * Rec) + (0.02 * Comps)
        Missed_Target_Points = (-0.02 * (Targets - Rec)) + (-0.01 * (Atts - Comps)) + (-0.02 * Sacks_Taken)
        
        YPC = (Rush_Yards / (Car + 1))
        YPR = (Air_Yards / (Rec + 1))
        YACavg = (YAC / (Rec + 1))
        YPTAvg = (Passing_Yards / (Comps + 1))
        
        Yard_Points = 0.5 * YPC + 0.6 * YPR + 0.4 * YACavg + 0.4 * YPTAvg
        Fumble_Points = (-1 * (Fumbs/(Car + Rec + 1))) + (-1 * (Interceptions_Thrown/(Comps + 1)))    
        
        Total_Points = round((Yard_Points + Touchdown_Points + Fumble_Points + Reception_Points + Missed_Target_Points) * (API/1000), 1)
        Database[ID] = Total_Points

    Create_Leaderboard("RPI Score", Database, Amount)
    
Players = Create_Database({"Position": ["WR", "RB", "TE", "QB"]}, 2026)

#Fantasy_Points(Players, 25)
#Breakout_Index(Players, 25)
Relative_Prime_Index(Players, 25)
    