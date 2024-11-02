from models.player import Player
from models.team import Team
from database.db_manager import DatabaseManager

class TransferController:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def buy_player(self, team_id, player_id, purchase_price):
        """
        Buy a player and add them to the specified team.
        """
        finance = self.db_manager.get_finance_by_team_id(team_id)
        if finance and finance['budget'] >= purchase_price:
            self.db_manager.update_finance_budget(team_id, finance['budget'] - purchase_price)
            self.db_manager.add_player_to_team(team_id, player_id)
            print(f"Player ID {player_id} bought by Team ID {team_id} for {purchase_price}.")
            return True
        else:
            print(f"Insufficient budget for Team ID {team_id} to buy Player ID {player_id}.")
            return False

    def sell_player(self, team_id, player_id, sell_price):
        """
        Sell a player from the specified team.
        """
        self.db_manager.remove_player_from_team(team_id, player_id)
        self.db_manager.update_finance_budget(team_id, self.db_manager.get_finance_by_team_id(team_id)['budget'] + sell_price)
        print(f"Player ID {player_id} sold by Team ID {team_id} for {sell_price}.")
        return True

    def negotiate_contract(self, player_id, new_contract_end, salary_increase):
        """
        Negotiate a new contract for a player.
        """
        player = self.db_manager.get_player_by_id(player_id)
        if player:
            self.db_manager.update_player_contract(player_id, new_contract_end)
            # Assume salary is part of budget; adjust finances accordingly
            team_id = self.db_manager.get_team_of_player(player_id)
            finance = self.db_manager.get_finance_by_team_id(team_id)
            if finance:
                self.db_manager.update_finance_expenses(team_id, salary_increase)
                print(f"Contract for Player ID {player_id} updated to end on {new_contract_end} with a salary increase of {salary_increase}.")
                return True
        print(f"Failed to negotiate contract for Player ID {player_id}.")
        return False

    def handle_transfer_deadline(self, current_date):
        """
        Handle transfer deadlines, potentially restricting transfers after the deadline.
        """
        # Placeholder for deadline logic
        print(f"Handling transfer deadline logic for date {current_date}.")
        # Implement logic to restrict or allow transfers based on the current date
        pass

    def list_available_players(self):
        """
        List all players not currently assigned to any team.
        """
        players = self.db_manager.get_available_players()
        available_players = [Player(p['name'], p['position'], p['skills'], p['morale'], p['contract_end']) for p in players]
        print(f"Retrieved {len(available_players)} available players.")
        return available_players
