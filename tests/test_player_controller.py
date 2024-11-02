import unittest
import os
from database.db_manager import DatabaseManager
from controllers.player_controller import PlayerController
from models.player import Player

class TestPlayerController(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Use a separate test database
        cls.test_db_path = 'savegames/test_game.db'
        # Ensure the test database does not already exist
        if os.path.exists(cls.test_db_path):
            os.remove(cls.test_db_path)
        cls.db_manager = DatabaseManager(db_path=cls.test_db_path)
        cls.player_controller = PlayerController(cls.db_manager)

    @classmethod
    def tearDownClass(cls):
        cls.db_manager.close()
        # Remove the test database after tests
        if os.path.exists(cls.test_db_path):
            os.remove(cls.test_db_path)

    def test_create_and_get_player(self):
        # Create a player
        player = self.player_controller.create_player(
            name="John Doe",
            position="Forward",
            skills=85,
            morale=90,
            contract_end=2025
        )
        self.assertIsNotNone(player, "Player should be created successfully.")
        self.assertIsNotNone(player.id, "Player ID should be set.")
        
        # Retrieve the player
        retrieved_player = self.player_controller.get_player(player.id)
        self.assertIsNotNone(retrieved_player, "Retrieved player should not be None.")
        self.assertEqual(retrieved_player.name, "John Doe")
        self.assertEqual(retrieved_player.position, "Forward")
        self.assertEqual(retrieved_player.skills, 85)
        self.assertEqual(retrieved_player.morale, 90)
        self.assertEqual(retrieved_player.contract_end, 2025)

    def test_update_player_skills(self):
        # Create a player
        player = self.player_controller.create_player(
            name="Jane Smith",
            position="Midfielder",
            skills=75,
            morale=80,
            contract_end=2024
        )
        self.assertIsNotNone(player, "Player should be created successfully.")
        
        # Update player skills
        result = self.player_controller.update_player_skills(player.id, 80)
        self.assertTrue(result, "Player skills should be updated successfully.")
        
        # Verify the update
        updated_player = self.player_controller.get_player(player.id)
        self.assertEqual(updated_player.skills, 80, "Player skills should be updated to 80.")

    def test_delete_player(self):
        # Create a player
        player = self.player_controller.create_player(
            name="Mike Johnson",
            position="Defender",
            skills=70,
            morale=85,
            contract_end=2023
        )
        self.assertIsNotNone(player, "Player should be created successfully.")
        
        # Delete the player
        result = self.player_controller.delete_player(player.id)
        self.assertTrue(result, "Player should be deleted successfully.")
        
        # Attempt to retrieve the deleted player
        deleted_player = self.player_controller.get_player(player.id)
        self.assertIsNone(deleted_player, "Player should no longer exist after deletion.")

if __name__ == '__main__':
    unittest.main()
