import NFLStatsAnalyzer as NFL
import time

indexes = ["Fantasy Points", "Breakout Index", "Relative Prime Index"]
index_book = dict()

def print_indexes(index_boo, indexe):
    # set-up
    print_line = "Indexes:\n"
    for indi in indexe: #Very recursive looking code, basically just splits all indexes into acrynoms so they can be indexed by both within the index book
        indi_parts = indi.split()
        print_line += indi + " ("
        indie = ""
        for indi_part in indi_parts:
            indie += indi_part[0]
        print_line += indie + ")\n"   
        
        index_boo[indi.lower()] = indi.lower()
        index_boo[indie.lower()] = indi.lower()
    
    print(print_line)

def get_season():
    Season1 = None
    while Season1 == None:
        try:
            Season1 = input("Enter starting season (1999-2026 or all/True): ").strip()
            if Season1.lower() == "all" or Season1.lower() == "true":
                print("Season interval to analyze is from 1999 to 2026.\n")
                return True
            else:
                if 1999 <= int(Season1) <= 2026:
                    Season1 = int(Season1)
                else:
                    Season1 = None
        except Exception as e:
            Season1 = None
            print("User Error: {}\nPlease retry.".format(e))
            continue
    
    Season2 = None
    while Season2 == None:
        try:
            Season2 = int(input("Enter ending season (1999-2026): ").strip())
            if 1999 <= int(Season2) <= 2026:
                Season2 = int(Season2)
            else:
                Season2 = None
        except Exception as e:
            print("User Error: {}\nPlease retry.".format(e))
            continue
        
    First = min(Season1, Season2)
    Last = max(Season1, Season2)
    print("Season interval to analyze is from {} to {}.\n".format(First, Last))
    
    return [First, Last]
    
def get_index(index_boo, indexe):
    
    print_indexes(index_book, indexes)
    
    Index = None
    while Index == None:
        try:
            Index = input("Enter desired index: ").strip().lower()
            
            if index_book[Index.lower()] == "fantasy points":
                Index = "Fantasy Points"
            elif index_book[Index.lower()] == "breakout index":
                Index = "Breakout Index"
            elif index_book[Index.lower()] == "relative prime index":
                Index = "Relative Prime Index"
            else:
                print("User Error: Unrecognized index.\nPlease retry.")    
        except Exception as e:
            Index = None
            print("User Error: Unrecognized index {}.\nPlease retry.".format(e))
            
    return Index

def get_amount(Plrs):
    Amount = None
    while Amount == None:
        try:
            Amount = input("Enter # of leaderboard entries (0-{}): ".format(len(Plrs))).strip()
            if Amount.lower() == "all" or Amount.lower() == "true" or Amount.lower() == "max":
                print("Fetching the top {} rankings...\n".format(len(Plrs)))
                return len(Plrs)
            else:
                if 0 <= int(Amount) <= len(Plrs):
                    Amount = int(Amount)
                else:
                    Amount = None
        except Exception as e:
            Amount = None
            print("User Error: {}\nPlease retry.".format(e))
            continue
        
    print("Fetching the top {} rankings...\n".format(Amount))
    
    return Amount
    
def get_filter(index_boo, indexe):
    pass
        
if __name__ == "__main__":
    while True:
        
        season = get_season() 
        index = get_index(index_book, indexes)
        
        print("Generating players...")
        
        Players = NFL.Create_Database({"Position": ["WR", "RB", "TE", "QB"]}, season)
        if len(Players) == 0:
            print("User Error: Zero players meet the criteria!")
            continue
        
        print("Players generated!\n")
        
        amount = get_amount(Players)
        
        if index == "Fantasy Points":
            NFL.Fantasy_Points(Players, amount)
        elif index == "Breakout Index":
            NFL.Breakout_Index(Players, amount)
        elif index == "Relative Prime Index":
            NFL.Relative_Prime_Index(Players, amount)
        
        print()