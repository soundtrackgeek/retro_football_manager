import pygame
from views.menu_view import MenuView
from views.team_selection_view import TeamSelectionView
from views.team_view import TeamView  # Import TeamView

class GameState:
    def __init__(self):
        self.current_view = "menu"
        self.selected_team_id = None

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Retro Football Manager")
        self.clock = pygame.time.Clock()
        self.game_state = GameState()
        self.menu_view = MenuView(self.screen)
        self.team_selection_view = TeamSelectionView(self.screen, self.game_state)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if self.game_state.current_view == "menu":
                    action = self.menu_view.handle_input(event)
                    if action == "Start Game":
                        self.game_state.current_view = "team_selection"
                    elif action == "Exit":
                        running = False

                elif self.game_state.current_view == "team_selection":
                    self.team_selection_view.handle_input(event)
                    if self.game_state.current_view != "team_selection":
                        # Transitioned to a new view (e.g., TeamView)
                        if isinstance(self.game_state.current_view, TeamView):
                            self.team_view = self.game_state.current_view

                elif isinstance(self.game_state.current_view, TeamView):
                    self.game_state.current_view.handle_input(event)

            if self.game_state.current_view == "menu":
                self.menu_view.draw()
            elif self.game_state.current_view == "team_selection":
                self.team_selection_view.draw()
            elif isinstance(self.game_state.current_view, TeamView):
                self.game_state.current_view.draw()

            self.clock.tick(60)

        pygame.quit()

def start_new_game():
    # ...existing code...
    db_manager.initialize_english_teams()
    # ...existing code...

if __name__ == "__main__":
    game = Game()
    game.run()
