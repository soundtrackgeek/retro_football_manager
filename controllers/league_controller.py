from models.league import League
from database.db_manager import DatabaseManager

class LeagueController:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def create_league(self, name, season):
        league = League(name, season)
        league.id = self.db_manager.add_league(name, season)
        print(f"League '{name}' for season '{season}' created successfully with ID {league.id}.")
        return league

    def get_league(self, league_id):
        league_data = self.db_manager.get_league_by_id(league_id)
        if league_data:
            league = League(league_data['name'], league_data['season'])
            league.id = league_data['id']
            print(f"Retrieved League: {league}.")
            return league
        else:
            print(f"No league found with ID {league_id}.")
            return None

    def update_league_name(self, league_id, new_name):
        self.db_manager.update_league_name(league_id, new_name)
        print(f"League ID {league_id} name updated to '{new_name}'.")

    def update_league_season(self, league_id, new_season):
        self.db_manager.update_league_season(league_id, new_season)
        print(f"League ID {league_id} season updated to '{new_season}'.")

    def delete_league(self, league_id):
        self.db_manager.delete_league(league_id)
        print(f"League ID {league_id} deleted successfully.")

    def list_all_leagues(self):
        leagues_data = self.db_manager.get_all_leagues()
        leagues = []
        for data in leagues_data:
            league = League(data['name'], data['season'])
            league.id = data['id']
            leagues.append(league)
        print(f"Retrieved {len(leagues)} leagues.")
        return leagues
