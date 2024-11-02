from models.finance import Finance
from database.db_manager import DatabaseManager

class FinanceController:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def create_finance_record(self, team_id, budget, revenue=0, expenses=0):
        finance = Finance(team_id, budget, revenue, expenses)
        finance.id = self.db_manager.add_finance(team_id, budget, revenue, expenses)
        print(f"Finance record for Team ID {team_id} created successfully with ID {finance.id}.")
        return finance

    def get_finance(self, team_id):
        finance_data = self.db_manager.get_finance_by_team_id(team_id)
        if finance_data:
            finance = Finance(
                team_id=finance_data['team_id'],
                budget=finance_data['budget'],
                revenue=finance_data['revenue'],
                expenses=finance_data['expenses']
            )
            finance.id = finance_data['id']
            print(f"Retrieved Finance: {finance}.")
            return finance
        else:
            print(f"No finance record found for Team ID {team_id}.")
            return None

    def update_budget(self, team_id, new_budget):
        self.db_manager.update_finance_budget(team_id, new_budget)
        print(f"Budget for Team ID {team_id} updated to {new_budget}.")

    def add_revenue(self, team_id, additional_revenue):
        self.db_manager.update_finance_revenue(team_id, additional_revenue)
        print(f"Revenue for Team ID {team_id} increased by {additional_revenue}.")

    def add_expenses(self, team_id, additional_expenses):
        self.db_manager.update_finance_expenses(team_id, additional_expenses)
        print(f"Expenses for Team ID {team_id} increased by {additional_expenses}.")

    def delete_finance_record(self, team_id):
        self.db_manager.delete_finance(team_id)
        print(f"Finance record for Team ID {team_id} deleted successfully.")
