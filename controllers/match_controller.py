from models.match import Match
from database.db_manager import DatabaseManager
import random
import datetime

class MatchController:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def create_match(self, home_team_id, away_team_id, date=None):
        if date is None:
            date = datetime.datetime.now().strftime("%Y-%m-%d")
        match_id = self.db_manager.add_match(home_team_id, away_team_id, date)
        match = Match(home_team_id, away_team_id, date)
        match.id = match_id
        print(f"Match created between Team ID {home_team_id} and Team ID {away_team_id} on {date} with Match ID {match_id}.")
        return match

    def get_match(self, match_id):
        match_data = self.db_manager.get_match_by_id(match_id)
        if match_data:
            match = Match(
                home_team=match_data['home_team_id'],
                away_team=match_data['away_team_id'],
                date=match_data['date'],
                home_score=match_data['home_score'],
                away_score=match_data['away_score']
            )
            match.id = match_data['id']
            print(f"Retrieved {match}.")
            return match
        else:
            print(f"No match found with ID {match_id}.")
            return None

    def simulate_match(self, match_id):
        match = self.get_match(match_id)
        if match:
            # Simple simulation logic: random scores
            match.home_score = random.randint(0, 5)
            match.away_score = random.randint(0, 5)
            self.db_manager.update_match_score(match_id, match.home_score, match.away_score)
            print(f"Match ID {match_id} simulated: {match.home_score} - {match.away_score}.")
            return match
        else:
            print(f"Cannot simulate match. Match with ID {match_id} does not exist.")
            return None

    def list_all_matches(self):
        matches = self.db_manager.get_all_matches()
        match_list = []
        for match_data in matches:
            match = Match(
                home_team=match_data['home_team_id'],
                away_team=match_data['away_team_id'],
                date=match_data['date'],
                home_score=match_data['home_score'],
                away_score=match_data['away_score']
            )
            match.id = match_data['id']
            match_list.append(match)
        print(f"Retrieved {len(match_list)} matches.")
        return match_list

    def delete_match(self, match_id):
        self.db_manager.delete_match(match_id)
        print(f"Match ID {match_id} deleted successfully.")
