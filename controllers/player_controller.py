from models.player import Player
from database.db_manager import DatabaseManager
from utils.logger import setup_logger

class PlayerController:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.logger = setup_logger('player_controller_logger', 'logs/player_controller.log')

    def create_player(self, name, position, skills, morale, contract_end):
        try:
            player = Player(name, position, skills, morale, contract_end)
            player.id = self.db_manager.add_player(name, position, skills, morale, contract_end)
            self.logger.info(f"Player '{name}' created successfully with ID {player.id}.")
            return player
        except Exception as e:
            self.logger.error(f"Failed to create player '{name}': {e}")
            return None

    def get_player(self, player_id):
        try:
            player_data = self.db_manager.get_player_by_id(player_id)
            if player_data:
                player = Player(
                    name=player_data['name'],
                    position=player_data['position'],
                    skills=player_data['skills'],
                    morale=player_data['morale'],
                    contract_end=player_data['contract_end']
                )
                player.id = player_data['id']
                self.logger.info(f"Retrieved player: {player}.")
                return player
            else:
                self.logger.warning(f"No player found with ID {player_id}.")
                return None
        except Exception as e:
            self.logger.error(f"Error retrieving player with ID {player_id}: {e}")
            return None

    def update_player_skills(self, player_id, new_skills):
        try:
            self.db_manager.update_player_skills(player_id, new_skills)
            self.logger.info(f"Player ID {player_id} skills updated to {new_skills}.")
            return True
        except Exception as e:
            self.logger.error(f"Error updating skills for player ID {player_id}: {e}")
            return False

    def update_player_morale(self, player_id, new_morale):
        try:
            self.db_manager.update_player_morale(player_id, new_morale)
            self.logger.info(f"Player ID {player_id} morale updated to {new_morale}.")
            return True
        except Exception as e:
            self.logger.error(f"Error updating morale for player ID {player_id}: {e}")
            return False

    def update_player_contract(self, player_id, new_contract_end):
        try:
            self.db_manager.update_player_contract(player_id, new_contract_end)
            self.logger.info(f"Player ID {player_id} contract end updated to {new_contract_end}.")
            return True
        except Exception as e:
            self.logger.error(f"Error updating contract for player ID {player_id}: {e}")
            return False

    def delete_player(self, player_id):
        try:
            self.db_manager.delete_player(player_id)
            self.logger.info(f"Player ID {player_id} deleted successfully.")
            return True
        except Exception as e:
            self.logger.error(f"Error deleting player ID {player_id}: {e}")
            return False
