from models.team import Team
from database.db_manager import DatabaseManager

class TeamController:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def create_team(self, name, formation, tactics):
        team = Team(name, formation, tactics)
        self.db_manager.add_team(name, formation, tactics)
        print(f"Team '{name}' created successfully.")
        return team

    def get_team(self, team_id):
        team_data = self.db_manager.get_team_by_id(team_id)
        if team_data:
            team = Team(team_data['name'], team_data['formation'], team_data['tactics'])
            team.id = team_data['id']
            print(f"Retrieved team '{team.name}' with ID {team.id}.")
            return team
        else:
            print(f"No team found with ID {team_id}.")
            return None

    def add_player_to_team(self, team_id, player):
        team = self.get_team(team_id)
        if team:
            team.add_player(player)
            self.db_manager.add_player_to_team(team_id, player.id)
            print(f"Player '{player.name}' added to team '{team.name}'.")
        else:
            print(f"Cannot add player. Team with ID {team_id} does not exist.")

    def remove_player_from_team(self, team_id, player_id):
        team = self.get_team(team_id)
        if team:
            team.remove_player(player_id)
            self.db_manager.remove_player_from_team(team_id, player_id)
            print(f"Player with ID {player_id} removed from team '{team.name}'.")
        else:
            print(f"Cannot remove player. Team with ID {team_id} does not exist.")

    def update_team_formation(self, team_id, new_formation):
        team = self.get_team(team_id)
        if team:
            self.db_manager.update_team_formation(team_id, new_formation)
            team.formation = new_formation
            print(f"Team '{team.name}' formation updated to '{new_formation}'.")
        else:
            print(f"Cannot update formation. Team with ID {team_id} does not exist.")

    def update_team_tactics(self, team_id, new_tactics):
        team = self.get_team(team_id)
        if team:
            self.db_manager.update_team_tactics(team_id, new_tactics)
            team.tactics = new_tactics
            print(f"Team '{team.name}' tactics updated to '{new_tactics}'.")
        else:
            print(f"Cannot update tactics. Team with ID {team_id} does not exist.")
