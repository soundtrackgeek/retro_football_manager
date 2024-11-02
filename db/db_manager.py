class DatabaseManager:
    def __init__(self):
        # Temporary hardcoded data until we implement actual database
        self.teams = [
            (1, "Arsenal"),
            (2, "Chelsea"),
            (3, "Liverpool"),
            (4, "Manchester United"),
            (5, "Manchester City"),
            (6, "Tottenham")
        ]

    def get_english_teams(self):
        return self.teams
