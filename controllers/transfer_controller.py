from models.player import Player
from models.team import Team
from database.db_manager import DatabaseManager
from utils.logger import setup_logger

class TransferController:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.logger = setup_logger('transfer_controller_logger', 'logs/transfer_controller.log')

    def buy_player(self, team_id, player_id, purchase_price):
        """
        Buy a player and add them to the specified team.
        """
        try:
            finance = self.db_manager.get_finance_by_team_id(team_id)
            if finance and finance['budget'] >= purchase_price:
                self.db_manager.update_finance_budget(team_id, finance['budget'] - purchase_price)
                self.db_manager.add_player_to_team(team_id, player_id)
                self.logger.info(f"Player ID {player_id} bought by Team ID {team_id} for {purchase_price}.")
                return True
            else:
                self.logger.warning(f"Insufficient budget for Team ID {team_id} to buy Player ID {player_id}.")
                return False
        except Exception as e:
            self.logger.error(f"Error buying Player ID {player_id} for Team ID {team_id}: {e}")
            return False

    def sell_player(self, team_id, player_id, sell_price):
        """
        Sell a player from the specified team.
        """
        try:
            self.db_manager.remove_player_from_team(team_id, player_id)
            finance = self.db_manager.get_finance_by_team_id(team_id)
            if finance:
                self.db_manager.update_finance_budget(team_id, finance['budget'] + sell_price)
                self.logger.info(f"Player ID {player_id} sold by Team ID {team_id} for {sell_price}.")
                return True
            else:
                self.logger.warning(f"No finance record found for Team ID {team_id} while selling Player ID {player_id}.")
                return False
        except Exception as e:
            self.logger.error(f"Error selling Player ID {player_id} from Team ID {team_id}: {e}")
            return False

    def negotiate_contract(self, player_id, new_contract_end, salary_increase):
        """
        Negotiate a new contract for a player.
        """
        try:
            player = self.db_manager.get_player_by_id(player_id)
            if player:
                self.db_manager.update_player_contract(player_id, new_contract_end)
                team_id = self.db_manager.get_team_of_player(player_id)
                if team_id:
                    self.db_manager.update_finance_expenses(team_id, salary_increase)
                    self.logger.info(f"Contract for Player ID {player_id} updated to end on {new_contract_end} with a salary increase of {salary_increase}.")
                    return True
            self.logger.warning(f"Failed to negotiate contract for Player ID {player_id}.")
            return False
        except Exception as e:
            self.logger.error(f"Error negotiating contract for Player ID {player_id}: {e}")
            return False

    def handle_transfer_deadline(self, current_date):
        """
        Handle transfer deadlines, potentially restricting transfers after the deadline.
        """
        try:
            # Placeholder for deadline logic
            self.logger.info(f"Handling transfer deadline logic for date {current_date}.")
            # Implement logic to restrict or allow transfers based on the current date
        except Exception as e:
            self.logger.error(f"Error handling transfer deadline for date {current_date}: {e}")

    def list_available_players(self):
        """
        List all players not currently assigned to any team.
        """
        try:
            players = self.db_manager.get_available_players()
            available_players = [Player(p['name'], p['position'], p['skills'], p['morale'], p['contract_end']) for p in players]
            self.logger.info(f"Retrieved {len(available_players)} available players.")
            return available_players
        except Exception as e:
            self.logger.error(f"Error listing available players: {e}")
            return []
