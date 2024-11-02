class Match:
    def __init__(self, home_team, away_team, date, home_score=0, away_score=0):
        self.id = None  # Will be set by the database
        self.home_team = home_team
        self.away_team = away_team
        self.date = date
        self.home_score = home_score
        self.away_score = away_score

    def simulate_match(self):
        # Placeholder for match simulation logic
        pass

    def __repr__(self):
        return (f"Match(id={self.id}, home_team='{self.home_team}', away_team='{self.away_team}', "
                f"date='{self.date}', home_score={self.home_score}, away_score={self.away_score})")
