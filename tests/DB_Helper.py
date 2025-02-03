import os
import sys

fpath = os.path.join(os.path.dirname(__file__), '../Models')
sys.path.append(fpath)
import User_Model, Game_Model, Scorecard_Model

def wipe_and_clean_tables(yahtzee_db_name, user_table_name, game_table_name, scorecard_table_name):
    yahtzee_db_name=f"{os.getcwd()}/../models/yahtzeeDB.db"
    User_Model.User(yahtzee_db_name, user_table_name).initialize_table()
    Game_Model.Game(yahtzee_db_name, game_table_name).initialize_table()
    Scorecard_Model.Scorecard(yahtzee_db_name, scorecard_table_name, user_table_name, game_table_name).initialize_table()
