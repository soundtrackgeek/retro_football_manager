from models.team import Team
from database.db_manager import DatabaseManager
from utils.logger import setup_logger

class TeamController:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.logger = setup_logger('team_controller_logger', 'logs/team_controller.log')

    def create_team(self, name, formation, tactics):
        team = Team(name, formation, tactics)
        try:
            team.id = self.db_manager.add_team(name, formation, tactics)
            self.logger.info(f"Team '{name}' created successfully with ID {team.id}.")
            return team
        except Exception as e:
            self.logger.error(f"Failed to create team '{name}': {e}")
            return None

    def get_team(self, team_id):
        try:
            team_data = self.db_manager.get_team_by_id(team_id)
            if team_data:
                team = Team(team_data['name'], team_data['formation'], team_data['tactics'])
                team.id = team_data['id']
                self.logger.info(f"Retrieved team: {team}.")
                return team
            else:
                self.logger.warning(f"No team found with ID {team_id}.")
                return None
        except Exception as e:
            self.logger.error(f"Error retrieving team with ID {team_id}: {e}")
            return None

    def add_player_to_team(self, team_id, player):
        try:
            team = self.get_team(team_id)
            if team:
                team.add_player(player)
                self.db_manager.add_player_to_team(team_id, player.id)
                self.logger.info(f"Player '{player.name}' (ID: {player.id}) added to team '{team.name}' (ID: {team.id}).")
                return True
            else:
                self.logger.warning(f"Cannot add player. Team with ID {team_id} does not exist.")
                return False
        except Exception as e:
            self.logger.error(f"Error adding player to team ID {team_id}: {e}")
            return False

    def remove_player_from_team(self, team_id, player_id):
        try:
            team = self.get_team(team_id)
            if team:
                team.remove_player(player_id)
                self.db_manager.remove_player_from_team(team_id, player_id)
                self.logger.info(f"Player ID {player_id} removed from team '{team.name}' (ID: {team.id}).")
                return True
            else:
                self.logger.warning(f"Cannot remove player. Team with ID {team_id} does not exist.")
                return False
        except Exception as e:
            self.logger.error(f"Error removing player ID {player_id} from team ID {team_id}: {e}")
            return False

    def update_team_formation(self, team_id, new_formation):
        try:
            team = self.get_team(team_id)
            if team:
                self.db_manager.update_team_formation(team_id, new_formation)
                team.formation = new_formation
                self.logger.info(f"Team '{team.name}' (ID: {team.id}) formation updated to '{new_formation}'.")
                return True
            else:
                self.logger.warning(f"Cannot update formation. Team with ID {team_id} does not exist.")
                return False
        except Exception as e:
            self.logger.error(f"Error updating formation for team ID {team_id}: {e}")
            return False

    def update_team_tactics(self, team_id, new_tactics):
        try:
            team = self.get_team(team_id)
            if team:
                self.db_manager.update_team_tactics(team_id, new_tactics)
                team.tactics = new_tactics
                self.logger.info(f"Team '{team.name}' (ID: {team.id}) tactics updated to '{new_tactics}'.")
                return True
            else:
                self.logger.warning(f"Cannot update tactics. Team with ID {team_id} does not exist.")
                return False
        except Exception as e:
            self.logger.error(f"Error updating tactics for team ID {team_id}: {e}")
            return False
