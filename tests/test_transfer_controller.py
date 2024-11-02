import unittest
import os
from database.db_manager import DatabaseManager
from controllers.transfer_controller import TransferController
from models.player import Player
from models.team import Team

class TestTransferController(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Use a separate test database
        cls.test_db_path = 'savegames/test_game.db'
        # Ensure the test database does not already exist
        if os.path.exists(cls.test_db_path):
            os.remove(cls.test_db_path)
        cls.db_manager = DatabaseManager(db_path=cls.test_db_path)
        cls.transfer_controller = TransferController(cls.db_manager)

        # Setup initial teams for testing
        cls.team1_id = cls.db_manager.add_team(name="Alpha FC", formation="4-4-2", tactics="Aggressive")
        cls.team2_id = cls.db_manager.add_team(name="Beta FC", formation="3-5-2", tactics="Defensive")

        # Add players
        cls.player1_id = cls.db_manager.add_player(name="John Doe", position="Forward", skills=85, morale=90, contract_end=2025)
        cls.player2_id = cls.db_manager.add_player(name="Jane Smith", position="Midfielder", skills=80, morale=85, contract_end=2024)
        cls.player3_id = cls.db_manager.add_player(name="Mike Johnson", position="Defender", skills=75, morale=80, contract_end=2023)

        # Add player1 to team1
        cls.db_manager.add_player_to_team(cls.team1_id, cls.player1_id)

    @classmethod
    def tearDownClass(cls):
        cls.db_manager.close()
        # Remove the test database after tests
        if os.path.exists(cls.test_db_path):
            os.remove(cls.test_db_path)

    def test_buy_player_successful(self):
        # Player2 is available
        result = self.transfer_controller.buy_player(team_id=self.team1_id, player_id=self.player2_id, purchase_price=100000)
        self.assertTrue(result, "Player should be bought successfully.")

        # Verify player2 is now part of team1
        cursor = self.db_manager.conn.cursor()
        cursor.execute("""
            SELECT * FROM team_players
            WHERE team_id = ? AND player_id = ?
        """, (self.team1_id, self.player2_id))
        association = cursor.fetchone()
        self.assertIsNotNone(association, "Player2 should be associated with Team1 after buying.")
        self.assertEqual(association['team_id'], self.team1_id)
        self.assertEqual(association['player_id'], self.player2_id)

    def test_buy_player_insufficient_budget(self):
        # Adjust team1 budget to below purchase price
        self.db_manager.update_finance_budget(self.team1_id, 50000)

        # Attempt to buy player3 with purchase_price higher than budget
        result = self.transfer_controller.buy_player(team_id=self.team1_id, player_id=self.player3_id, purchase_price=100000)
        self.assertFalse(result, "Player buy should fail due to insufficient budget.")

    def test_sell_player_successful(self):
        # Player1 is part of team1
        result = self.transfer_controller.sell_player(team_id=self.team1_id, player_id=self.player1_id, sell_price=80000)
        self.assertTrue(result, "Player should be sold successfully.")

        # Verify player1 is no longer part of team1
        cursor = self.db_manager.conn.cursor()
        cursor.execute("""
            SELECT * FROM team_players
            WHERE team_id = ? AND player_id = ?
        """, (self.team1_id, self.player1_id))
        association = cursor.fetchone()
        self.assertIsNone(association, "Player1 should be removed from Team1 after selling.")

    def test_negotiate_contract_successful(self):
        # Player2 was bought by team1
        result = self.transfer_controller.negotiate_contract(player_id=self.player2_id, new_contract_end=2026, salary_increase=20000)
        self.assertTrue(result, "Contract negotiation should be successful.")

        # Verify contract end
        player = self.db_manager.get_player_by_id(self.player2_id)
        self.assertEqual(player['contract_end'], 2026, "Player2's contract end should be updated to 2026.")

        # Verify salary increase reflected in budget
        finance = self.db_manager.get_finance_by_team_id(self.team1_id)
        expected_budget = finance['budget']  # Original budget minus purchase_price plus salary_increase
        self.assertEqual(finance['budget'], 50000 - 100000 + 20000, "Team1's budget should reflect the salary increase.")

    def test_handle_transfer_deadline(self):
        # Assuming transfer deadline is handled via a flag or date comparison
        current_date = "2024-01-31"
        self.transfer_controller.handle_transfer_deadline(current_date)
        # Since it's a placeholder, just ensure no exceptions are raised
        # Further implementation needed to check transfer restrictions
        self.assertTrue(True, "Transfer deadline handled without errors.")

    def test_list_available_players(self):
        # Player3 is available
        available_players = self.transfer_controller.list_available_players()
        player_ids = [player.id for player in available_players]
        self.assertIn(self.player3_id, player_ids, "Player3 should be listed as available.")
        self.assertNotIn(self.player1_id, player_ids, "Player1 should not be listed as available since sold.")
        self.assertNotIn(self.player2_id, player_ids, "Player2 should not be listed as available since bought.")

    def test_buy_player_after_negotiate_contract(self):
        # Player2's contract was updated
        # Attempt to buy player3 again with sufficient budget
        self.db_manager.update_finance_budget(self.team1_id, 200000)  # Ensure sufficient budget
        result = self.transfer_controller.buy_player(team_id=self.team1_id, player_id=self.player3_id, purchase_price=100000)
        self.assertTrue(result, "Player3 should be bought successfully after adjusting budget.")

        # Verify association
        cursor = self.db_manager.conn.cursor()
        cursor.execute("""
            SELECT * FROM team_players
            WHERE team_id = ? AND player_id = ?
        """, (self.team1_id, self.player3_id))
        association = cursor.fetchone()
        self.assertIsNotNone(association, "Player3 should be associated with Team1 after buying.")
        self.assertEqual(association['team_id'], self.team1_id)
        self.assertEqual(association['player_id'], self.player3_id)

if __name__ == '__main__':
    unittest.main()
