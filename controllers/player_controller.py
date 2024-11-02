from models.player import Player
from database.db_manager import DatabaseManager

class PlayerController:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def create_player(self, name, position, skills, morale, contract_end):
        player = Player(name, position, skills, morale, contract_end)
        player.id = self.db_manager.add_player(name, position, skills, morale, contract_end)
        print(f"Player '{name}' created successfully with ID {player.id}.")
        return player

    def get_player(self, player_id):
        players = self.db_manager.get_all_players()
        for player_data in players:
            if player_data[0] == player_id:
                player = Player(player_data[1], player_data[2], player_data[3], player_data[4], player_data[5])
                player.id = player_data[0]
                print(f"Retrieved {player}.")
                return player
        print(f"No player found with ID {player_id}.")
        return None

    def update_player_skills(self, player_id, new_skills):
        self.db_manager.update_player_skills(player_id, new_skills)
        print(f"Player ID {player_id} skills updated to {new_skills}.")

    def update_player_morale(self, player_id, new_morale):
        self.db_manager.update_player_morale(player_id, new_morale)
        print(f"Player ID {player_id} morale updated to {new_morale}.")

    def update_player_contract(self, player_id, new_contract_end):
        self.db_manager.update_player_contract(player_id, new_contract_end)
        print(f"Player ID {player_id} contract end updated to {new_contract_end}.")

    def delete_player(self, player_id):
        self.db_manager.delete_player(player_id)
        print(f"Player ID {player_id} deleted successfully.")
