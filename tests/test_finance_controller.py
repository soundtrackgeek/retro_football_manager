import unittest
import os
from database.db_manager import DatabaseManager
from controllers.finance_controller import FinanceController
from models.finance import Finance

class TestFinanceController(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Use a separate test database
        cls.test_db_path = 'savegames/test_game.db'
        # Ensure the test database does not already exist
        if os.path.exists(cls.test_db_path):
            os.remove(cls.test_db_path)
        cls.db_manager = DatabaseManager(db_path=cls.test_db_path)
        cls.finance_controller = FinanceController(cls.db_manager)
        
        # Setup initial team for testing
        cls.team_id = cls.db_manager.add_team(name="Test FC", formation="4-4-2", tactics="Balanced")
        cls.db_manager.add_finance(team_id=cls.team_id, budget=1000000, revenue=500000, expenses=300000)

    @classmethod
    def tearDownClass(cls):
        cls.db_manager.close()
        # Remove the test database after tests
        if os.path.exists(cls.test_db_path):
            os.remove(cls.test_db_path)

    def test_create_finance_record(self):
        # Create a new finance record
        finance = self.finance_controller.create_finance_record(
            team_id=self.team_id,
            budget=1500000,
            revenue=600000,
            expenses=350000
        )
        self.assertIsNotNone(finance, "Finance record should be created successfully.")
        self.assertIsNotNone(finance.id, "Finance ID should be set.")

    def test_get_finance(self):
        # Retrieve existing finance record
        finance = self.finance_controller.get_finance(self.team_id)
        self.assertIsNotNone(finance, "Finance record should be retrieved successfully.")
        self.assertEqual(finance.team_id, self.team_id)
        self.assertEqual(finance.budget, 1000000)
        self.assertEqual(finance.revenue, 500000)
        self.assertEqual(finance.expenses, 300000)

    def test_update_budget(self):
        # Update budget
        result = self.finance_controller.update_budget(self.team_id, 1200000)
        self.assertTrue(result, "Budget should be updated successfully.")
        
        # Verify update
        finance = self.finance_controller.get_finance(self.team_id)
        self.assertEqual(finance.budget, 1200000, "Budget should be updated to 1200000.")

    def test_add_revenue(self):
        # Add revenue
        result = self.finance_controller.add_revenue(self.team_id, 200000)
        self.assertTrue(result, "Revenue should be added successfully.")
        
        # Verify update
        finance = self.finance_controller.get_finance(self.team_id)
        self.assertEqual(finance.revenue, 700000, "Revenue should be updated to 700000.")
        self.assertEqual(finance.budget, 1200000 + 200000, "Budget should be updated to 1400000.")

    def test_add_expenses(self):
        # Add expenses
        result = self.finance_controller.add_expenses(self.team_id, 50000)
        self.assertTrue(result, "Expenses should be added successfully.")
        
        # Verify update
        finance = self.finance_controller.get_finance(self.team_id)
        self.assertEqual(finance.expenses, 350000, "Expenses should be updated to 350000.")
        self.assertEqual(finance.budget, 1400000 - 50000, "Budget should be updated to 1350000.")

    def test_delete_finance_record(self):
        # Delete finance record
        result = self.finance_controller.delete_finance_record(self.team_id)
        self.assertTrue(result, "Finance record should be deleted successfully.")
        
        # Verify deletion
        finance = self.finance_controller.get_finance(self.team_id)
        self.assertIsNone(finance, "Finance record should no longer exist after deletion.")

if __name__ == '__main__':
    unittest.main()
