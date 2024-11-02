import unittest
import os
from database.db_manager import DatabaseManager
from controllers.team_controller import TeamController
from models.team import Team

class TestTeamController(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Use a separate test database
        cls.test_db_path = 'savegames/test_game.db'
        # Ensure the test database does not already exist
        if os.path.exists(cls.test_db_path):
            os.remove(cls.test_db_path)
        cls.db_manager = DatabaseManager(db_path=cls.test_db_path)
        cls.team_controller = TeamController(cls.db_manager)

    @classmethod
    def tearDownClass(cls):
        cls.db_manager.close()
        # Remove the test database after tests
        if os.path.exists(cls.test_db_path):
            os.remove(cls.test_db_path)

    def test_create_and_get_team(self):
        # Create a team
        team = self.team_controller.create_team(
            name="Eagles FC",
            formation="4-4-2",
            tactics="Offensive"
        )
        self.assertIsNotNone(team, "Team should be created successfully.")
        self.assertIsNotNone(team.id, "Team ID should be set.")
        
        # Retrieve the team
        retrieved_team = self.team_controller.get_team(team.id)
        self.assertIsNotNone(retrieved_team, "Retrieved team should not be None.")
        self.assertEqual(retrieved_team.name, "Eagles FC")
        self.assertEqual(retrieved_team.formation, "4-4-2")
        self.assertEqual(retrieved_team.tactics, "Offensive")

    def test_add_and_remove_player_to_team(self):
        # Create a team
        team = self.team_controller.create_team(
            name="Lions FC",
            formation="3-5-2",
            tactics="Defensive"
        )
        self.assertIsNotNone(team, "Team should be created successfully.")

        # Create a player
        player = self.db_manager.add_player(
            name="Alex Brown",
            position="Goalkeeper",
            skills=88,
            morale=92,
            contract_end=2026
        )
        self.assertIsNotNone(player, "Player should be created successfully.")
        
        # Add player to team
        result = self.team_controller.add_player_to_team(team.id, player)
        self.assertTrue(result, "Player should be added to the team successfully.")
        
        # Verify association
        team_data = self.db_manager.get_team_by_id(team.id)
        self.assertIsNotNone(team_data, "Team data should be retrieved successfully.")
        
        # Remove player from team
        result = self.team_controller.remove_player_from_team(team.id, player.id)
        self.assertTrue(result, "Player should be removed from the team successfully.")
        
        # Verify removal
        team_data = self.db_manager.get_team_by_id(team.id)
        # Assuming get_team_by_id does not return players, check via db_manager
        cursor = self.db_manager.conn.cursor()
        cursor.execute("""
            SELECT * FROM team_players
            WHERE team_id = ? AND player_id = ?
        """, (team.id, player.id))
        association = cursor.fetchone()
        self.assertIsNone(association, "Player should be removed from the team.")

    def test_update_team_formation_and_tactics(self):
        # Create a team
        team = self.team_controller.create_team(
            name="Tigers FC",
            formation="4-3-3",
            tactics="Balanced"
        )
        self.assertIsNotNone(team, "Team should be created successfully.")

        # Update formation
        result = self.team_controller.update_team_formation(team.id, "3-4-3")
        self.assertTrue(result, "Team formation should be updated successfully.")
        
        # Update tactics
        result = self.team_controller.update_team_tactics(team.id, "Aggressive")
        self.assertTrue(result, "Team tactics should be updated successfully.")
        
        # Verify updates
        updated_team = self.team_controller.get_team(team.id)
        self.assertEqual(updated_team.formation, "3-4-3")
        self.assertEqual(updated_team.tactics, "Aggressive")

if __name__ == '__main__':
    unittest.main()
