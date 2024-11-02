import unittest
import os
from database.db_manager import DatabaseManager
from models.player import Player
from models.team import Team

class TestDatabaseManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Use a separate test database
        cls.test_db_path = 'savegames/test_game.db'
        # Ensure the test database does not already exist
        if os.path.exists(cls.test_db_path):
            os.remove(cls.test_db_path)
        cls.db_manager = DatabaseManager(db_path=cls.test_db_path)

    @classmethod
    def tearDownClass(cls):
        cls.db_manager.close()
        # Remove the test database after tests
        if os.path.exists(cls.test_db_path):
            os.remove(cls.test_db_path)

    def test_add_and_get_player(self):
        # Add a player
        player_id = self.db_manager.add_player(
            name="John Doe",
            position="Forward",
            skills=85,
            morale=90,
            contract_end=2025
        )
        self.assertIsNotNone(player_id, "Player ID should not be None after adding.")

        # Retrieve the player
        player = self.db_manager.get_player_by_id(player_id)
        self.assertIsNotNone(player, "Retrieved player should not be None.")
        self.assertEqual(player['name'], "John Doe")
        self.assertEqual(player['position'], "Forward")
        self.assertEqual(player['skills'], 85)
        self.assertEqual(player['morale'], 90)
        self.assertEqual(player['contract_end'], 2025)

    def test_update_player_skills(self):
        # Add a player
        player_id = self.db_manager.add_player(
            name="Jane Smith",
            position="Midfielder",
            skills=75,
            morale=80,
            contract_end=2024
        )
        self.assertIsNotNone(player_id, "Player ID should not be None after adding.")

        # Update player skills
        self.db_manager.update_player_skills(player_id, 80)

        # Retrieve and check
        player = self.db_manager.get_player_by_id(player_id)
        self.assertEqual(player['skills'], 80, "Player skills should be updated to 80.")

    def test_delete_player(self):
        # Add a player
        player_id = self.db_manager.add_player(
            name="Mike Johnson",
            position="Defender",
            skills=70,
            morale=85,
            contract_end=2023
        )
        self.assertIsNotNone(player_id, "Player ID should not be None after adding.")

        # Delete the player
        self.db_manager.delete_player(player_id)

        # Try to retrieve
        player = self.db_manager.get_player_by_id(player_id)
        self.assertIsNone(player, "Player should be None after deletion.")

    def test_add_and_get_team(self):
        # Add a team
        team_id = self.db_manager.add_team(
            name="Eagles FC",
            formation="4-4-2",
            tactics="Aggressive"
        )
        self.assertIsNotNone(team_id, "Team ID should not be None after adding.")

        # Retrieve the team
        team = self.db_manager.get_team_by_id(team_id)
        self.assertIsNotNone(team, "Retrieved team should not be None.")
        self.assertEqual(team['name'], "Eagles FC")
        self.assertEqual(team['formation'], "4-4-2")
        self.assertEqual(team['tactics'], "Aggressive")

    def test_add_player_to_team(self):
        # Add a team
        team_id = self.db_manager.add_team(
            name="Lions FC",
            formation="3-5-2",
            tactics="Defensive"
        )
        self.assertIsNotNone(team_id, "Team ID should not be None after adding.")

        # Add a player
        player_id = self.db_manager.add_player(
            name="Alex Brown",
            position="Goalkeeper",
            skills=88,
            morale=92,
            contract_end=2026
        )
        self.assertIsNotNone(player_id, "Player ID should not be None after adding.")

        # Add player to team
        self.db_manager.add_player_to_team(team_id, player_id)

        # Verify association
        cursor = self.db_manager.conn.cursor()
        cursor.execute("""
            SELECT * FROM team_players
            WHERE team_id = ? AND player_id = ?
        """, (team_id, player_id))
        association = cursor.fetchone()
        self.assertIsNotNone(association, "Player should be associated with the team.")
        self.assertEqual(association['team_id'], team_id)
        self.assertEqual(association['player_id'], player_id)

    def test_remove_player_from_team(self):
        # Add a team
        team_id = self.db_manager.add_team(
            name="Tigers FC",
            formation="4-3-3",
            tactics="Balanced"
        )
        self.assertIsNotNone(team_id, "Team ID should not be None after adding.")

        # Add a player
        player_id = self.db_manager.add_player(
            name="Sam Wilson",
            position="Striker",
            skills=82,
            morale=88,
            contract_end=2024
        )
        self.assertIsNotNone(player_id, "Player ID should not be None after adding.")

        # Add player to team
        self.db_manager.add_player_to_team(team_id, player_id)

        # Remove player from team
        self.db_manager.remove_player_from_team(team_id, player_id)

        # Verify removal
        cursor = self.db_manager.conn.cursor()
        cursor.execute("""
            SELECT * FROM team_players
            WHERE team_id = ? AND player_id = ?
        """, (team_id, player_id))
        association = cursor.fetchone()
        self.assertIsNone(association, "Player should be removed from the team.")

if __name__ == '__main__':
    unittest.main()
