import unittest
import os
from database.db_manager import DatabaseManager
from controllers.match_controller import MatchController
from models.match import Match

class TestMatchController(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Use a separate test database
        cls.test_db_path = 'savegames/test_game.db'
        # Ensure the test database does not already exist
        if os.path.exists(cls.test_db_path):
            os.remove(cls.test_db_path)
        cls.db_manager = DatabaseManager(db_path=cls.test_db_path)
        cls.match_controller = MatchController(cls.db_manager)
        cls.team_controller = cls.db_manager  # Assuming teams are managed directly via db_manager for testing

        # Setup initial teams for testing
        cls.team1_id = cls.db_manager.add_team(name="Eagles FC", formation="4-4-2", tactics="Offensive")
        cls.team2_id = cls.db_manager.add_team(name="Lions FC", formation="3-5-2", tactics="Defensive")

    @classmethod
    def tearDownClass(cls):
        cls.db_manager.close()
        # Remove the test database after tests
        if os.path.exists(cls.test_db_path):
            os.remove(cls.test_db_path)

    def test_create_and_get_match(self):
        # Create a match
        match = self.match_controller.create_match(
            home_team_id=self.team1_id,
            away_team_id=self.team2_id,
            date="2024-05-15"
        )
        self.assertIsNotNone(match, "Match should be created successfully.")
        self.assertIsNotNone(match.id, "Match ID should be set.")

        # Retrieve the match
        retrieved_match = self.match_controller.get_match(match.id)
        self.assertIsNotNone(retrieved_match, "Retrieved match should not be None.")
        self.assertEqual(retrieved_match.home_team, self.team1_id)
        self.assertEqual(retrieved_match.away_team, self.team2_id)
        self.assertEqual(retrieved_match.date, "2024-05-15")
        self.assertEqual(retrieved_match.home_score, 0)
        self.assertEqual(retrieved_match.away_score, 0)

    def test_simulate_match(self):
        # Create a match
        match = self.match_controller.create_match(
            home_team_id=self.team1_id,
            away_team_id=self.team2_id,
            date="2024-06-20"
        )
        self.assertIsNotNone(match, "Match should be created successfully.")

        # Simulate the match
        simulated_match = self.match_controller.simulate_match(match.id)
        self.assertIsNotNone(simulated_match, "Simulated match should not be None.")
        self.assertGreaterEqual(simulated_match.home_score, 0, "Home score should be non-negative.")
        self.assertGreaterEqual(simulated_match.away_score, 0, "Away score should be non-negative.")

    def test_delete_match(self):
        # Create a match
        match = self.match_controller.create_match(
            home_team_id=self.team1_id,
            away_team_id=self.team2_id,
            date="2024-07-10"
        )
        self.assertIsNotNone(match, "Match should be created successfully.")

        # Delete the match
        result = self.match_controller.delete_match(match.id)
        self.assertTrue(result, "Match should be deleted successfully.")

        # Attempt to retrieve the deleted match
        deleted_match = self.match_controller.get_match(match.id)
        self.assertIsNone(deleted_match, "Match should no longer exist after deletion.")

    def test_list_all_matches(self):
        # Ensure no matches exist initially
        matches = self.match_controller.list_all_matches()
        initial_count = len(matches)
        
        # Create multiple matches
        match1 = self.match_controller.create_match(
            home_team_id=self.team1_id,
            away_team_id=self.team2_id,
            date="2024-08-05"
        )
        match2 = self.match_controller.create_match(
            home_team_id=self.team2_id,
            away_team_id=self.team1_id,
            date="2024-09-15"
        )
        self.assertIsNotNone(match1, "First match should be created successfully.")
        self.assertIsNotNone(match2, "Second match should be created successfully.")

        # List all matches
        matches = self.match_controller.list_all_matches()
        self.assertEqual(len(matches), initial_count + 2, "Should retrieve two additional matches.")

if __name__ == '__main__':
    unittest.main()
