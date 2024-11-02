import pygame
from database.db_manager import DatabaseManager
from views.team_view import TeamView  # Import TeamView

class TeamSelectionView:
    def __init__(self, screen, game_state):
        self.screen = screen
        self.game_state = game_state
        self.db_manager = DatabaseManager()
        self.font = pygame.font.Font(None, 36)
        self.selected_team_index = 0
        self.teams = []
        self.load_teams()

    def load_teams(self):
        self.teams = self.db_manager.get_english_teams()
        if not self.teams:
            # Add a default team if no teams exist
            team_id = self.db_manager.add_team("Your Team", "4-4-2", "Balanced")
            self.teams = self.db_manager.get_english_teams()

    def draw(self):
        self.screen.fill((0, 0, 0))  # Black background
        
        if not self.teams:
            text = self.font.render("No teams available", True, (255, 255, 255))
            self.screen.blit(text, (400 - text.get_width() // 2, 300))
            return

        y_position = 200
        for i, team in enumerate(self.teams):
            color = (255, 255, 0) if i == self.selected_team_index else (255, 255, 255)
            team_text = self.font.render(team['name'], True, color)  # Use team['name'] instead of team[1]
            x_position = 400 - team_text.get_width() // 2
            self.screen.blit(team_text, (x_position, y_position))
            y_position += 50

        pygame.display.flip()

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_team_index = (self.selected_team_index - 1) % len(self.teams)
            elif event.key == pygame.K_DOWN:
                self.selected_team_index = (self.selected_team_index + 1) % len(self.teams)
            elif event.key == pygame.K_RETURN:
                if self.teams:
                    selected_team = self.teams[self.selected_team_index]
                    self.game_state.selected_team_id = selected_team['id']
                    # Transition to the team view
                    self.game_state.current_view = TeamView(self.screen, self.game_state)