import os
import sys

fpath = os.path.join(os.path.dirname(__file__), '../Models')
sys.path.append(fpath)
print("-############-")
print(os.path.dirname(__file__), '../Models')
print("-############-")
import UserModel, GameModel, ScorecardModel

def wipe_and_clean_tables(yahtzee_db_name):
    yahtzee_db_name=f"{os.getcwd()}/models/yahtzeeDB.db"
    print("yahtzee_db_name", yahtzee_db_name)
    user_table_name = "users"
    game_table_name = "games"
    scorecard_table_name = "scorecard"
    UserModel.User(yahtzee_db_name, user_table_name).initialize_table()
    GameModel.Game(yahtzee_db_name, game_table_name).initialize_table()
    ScorecardModel.Scorecard(yahtzee_db_name, scorecard_table_name, user_table_name, game_table_name).initialize_table()
