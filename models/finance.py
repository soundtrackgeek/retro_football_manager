class Finance:
    def __init__(self, team_id, budget, revenue=0, expenses=0):
        self.id = None  # Will be set by the database
        self.team_id = team_id
        self.budget = budget
        self.revenue = revenue
        self.expenses = expenses

    def update_budget(self, amount):
        self.budget += amount
        print(f"Budget updated by {amount}. New budget: {self.budget}")

    def add_revenue(self, amount):
        self.revenue += amount
        self.budget += amount
        print(f"Revenue increased by {amount}. Total revenue: {self.revenue}. New budget: {self.budget}")

    def add_expenses(self, amount):
        self.expenses += amount
        self.budget -= amount
        print(f"Expenses increased by {amount}. Total expenses: {self.expenses}. New budget: {self.budget}")

    def __repr__(self):
        return (f"Finance(id={self.id}, team_id={self.team_id}, budget={self.budget}, "
                f"revenue={self.revenue}, expenses={self.expenses})")
