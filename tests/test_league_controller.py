import unittest
import os
from database.db_manager import DatabaseManager
from controllers.league_controller import LeagueController
from models.league import League

class TestLeagueController(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Use a separate test database
        cls.test_db_path = 'savegames/test_game.db'
        # Ensure the test database does not already exist
        if os.path.exists(cls.test_db_path):
            os.remove(cls.test_db_path)
        cls.db_manager = DatabaseManager(db_path=cls.test_db_path)
        cls.league_controller = LeagueController(cls.db_manager)

    @classmethod
    def tearDownClass(cls):
        cls.db_manager.close()
        # Remove the test database after tests
        if os.path.exists(cls.test_db_path):
            os.remove(cls.test_db_path)

    def test_create_and_get_league(self):
        # Create a league
        league = self.league_controller.create_league(
            name="Premier League",
            season="2024/2025"
        )
        self.assertIsNotNone(league, "League should be created successfully.")
        self.assertIsNotNone(league.id, "League ID should be set.")
        
        # Retrieve the league
        retrieved_league = self.league_controller.get_league(league.id)
        self.assertIsNotNone(retrieved_league, "Retrieved league should not be None.")
        self.assertEqual(retrieved_league.name, "Premier League")
        self.assertEqual(retrieved_league.season, "2024/2025")

    def test_update_league_name_and_season(self):
        # Create a league
        league = self.league_controller.create_league(
            name="La Liga",
            season="2023/2024"
        )
        self.assertIsNotNone(league, "League should be created successfully.")
        
        # Update league name
        result = self.league_controller.update_league_name(league.id, "La Liga Santander")
        self.assertTrue(result, "League name should be updated successfully.")
        
        # Update league season
        result = self.league_controller.update_league_season(league.id, "2024/2025")
        self.assertTrue(result, "League season should be updated successfully.")
        
        # Verify updates
        updated_league = self.league_controller.get_league(league.id)
        self.assertEqual(updated_league.name, "La Liga Santander")
        self.assertEqual(updated_league.season, "2024/2025")

    def test_delete_league(self):
        # Create a league
        league = self.league_controller.create_league(
            name="Bundesliga",
            season="2024/2025"
        )
        self.assertIsNotNone(league, "League should be created successfully.")
        
        # Delete the league
        result = self.league_controller.delete_league(league.id)
        self.assertTrue(result, "League should be deleted successfully.")
        
        # Attempt to retrieve the deleted league
        deleted_league = self.league_controller.get_league(league.id)
        self.assertIsNone(deleted_league, "League should no longer exist after deletion.")

    def test_list_all_leagues(self):
        # Ensure no leagues exist initially
        leagues = self.league_controller.list_all_leagues()
        initial_count = len(leagues)
        
        # Create multiple leagues
        league1 = self.league_controller.create_league(
            name="Serie A",
            season="2024/2025"
        )
        league2 = self.league_controller.create_league(
            name="Ligue 1",
            season="2024/2025"
        )
        self.assertIsNotNone(league1, "First league should be created successfully.")
        self.assertIsNotNone(league2, "Second league should be created successfully.")

        # List all leagues
        leagues = self.league_controller.list_all_leagues()
        self.assertEqual(len(leagues), initial_count + 2, "Should retrieve two additional leagues.")

if __name__ == '__main__':
    unittest.main()
