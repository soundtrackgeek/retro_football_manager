class League:
    def __init__(self, name, season):
        self.id = None  # Will be set by the database
        self.name = name
        self.season = season
        self.teams = []  # List of Team instances
        self.standings = {}  # Dictionary to track team standings

    def add_team(self, team):
        if isinstance(team, Team):
            self.teams.append(team)
            print(f"Team '{team.name}' added to league '{self.name}'.")
        else:
            print("Only Team instances can be added to the league.")

    def update_standings(self):
        # Placeholder for standings update logic
        pass

    def __repr__(self):
        return f"League(id={self.id}, name='{self.name}', season='{self.season}', teams={len(self.teams)})"
