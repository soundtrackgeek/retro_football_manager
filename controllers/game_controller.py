import pygame
from views.menu_view import MenuView
from controllers.team_controller import TeamController
from controllers.player_controller import PlayerController
from controllers.match_controller import MatchController
from controllers.league_controller import LeagueController
from controllers.finance_controller import FinanceController
from database.db_manager import DatabaseManager

class GameController:
    def __init__(self):
        # Initialize game state and resources
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Retro Football Manager")
        self.clock = pygame.time.Clock()
        self.running = True

        # Initialize DatabaseManager
        self.db_manager = DatabaseManager()

        # Initialize Controllers
        self.team_controller = TeamController(self.db_manager)
        self.player_controller = PlayerController(self.db_manager)
        self.match_controller = MatchController(self.db_manager)
        self.league_controller = LeagueController(self.db_manager)
        self.finance_controller = FinanceController(self.db_manager)

        # Initialize Views
        self.menu_view = MenuView(self.screen)

    def start_game(self):
        while self.running:
            selected_option = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    selected_option = self.menu_view.handle_input(event)

            if selected_option:
                self.handle_menu_selection(selected_option)

            self.update()
            self.render()
            self.clock.tick(60)  # Limit to 60 FPS

        self.db_manager.close()
        pygame.quit()

    def handle_menu_selection(self, selection):
        if selection == "Start Game":
            print("Starting a new game...")
            # Initialize or reset game state here
            # For example, create a default team, league, etc.
        elif selection == "Load Game":
            print("Loading game...")
            # Implement load game functionality
        elif selection == "Settings":
            print("Opening settings...")
            # Implement settings functionality
        elif selection == "Exit":
            print("Exiting game...")
            self.running = False

    def update(self):
        # Update game state if needed
        pass

    def render(self):
        # Render the current view
        self.menu_view.display_menu()
        pygame.display.flip()

if __name__ == '__main__':
    game = GameController()
    game.start_game()
