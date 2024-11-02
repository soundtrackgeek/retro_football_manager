import pygame
from views.menu_view import MenuView
from views.team_view import TeamView
from views.player_view import PlayerView
from views.match_view import MatchView
from views.league_view import LeagueView
from views.finance_view import FinanceView
from views.settings_view import SettingsView
from views.transfer_view import TransferView
from controllers.team_controller import TeamController
from controllers.player_controller import PlayerController
from controllers.match_controller import MatchController
from controllers.league_controller import LeagueController
from controllers.finance_controller import FinanceController
from controllers.transfer_controller import TransferController
from controllers.settings_controller import SettingsController
from database.db_manager import DatabaseManager
from utils.logger import setup_logger

class GameController:
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Retro Football Manager")
        self.clock = pygame.time.Clock()
        self.running = True

        # Initialize Logger
        self.logger = setup_logger('game_controller_logger', 'logs/game_controller.log')

        # Initialize DatabaseManager
        self.db_manager = DatabaseManager()

        # Initialize Controllers
        self.team_controller = TeamController(self.db_manager)
        self.player_controller = PlayerController(self.db_manager)
        self.match_controller = MatchController(self.db_manager)
        self.league_controller = LeagueController(self.db_manager)
        self.finance_controller = FinanceController(self.db_manager)
        self.transfer_controller = TransferController(self.db_manager)
        self.settings_controller = SettingsController(self.db_manager, None)  # SettingsView will be set later

        # Initialize Views
        self.menu_view = MenuView(self.screen)
        self.team_view = TeamView(self.screen)
        self.player_view = PlayerView(self.screen)
        self.match_view = MatchView(self.screen)
        self.league_view = LeagueView(self.screen)
        self.finance_view = FinanceView(self.screen)
        self.settings_view = SettingsView(self.screen)
        self.transfer_view = TransferView(self.screen)

        # Link SettingsController with SettingsView
        self.settings_controller.settings_view = self.settings_view

        # Set the initial view to the main menu
        self.current_view = self.menu_view

    def start_game(self):
        self.logger.info("Game started.")
        while self.running:
            selected_option = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.logger.info("Game exited by user.")
                else:
                    selected_option = self.current_view.handle_input(event)

            if selected_option:
                self.logger.info(f"Menu selection: {selected_option}")
                self.handle_selection(selected_option)

            self.update()
            self.render()
            self.clock.tick(60)  # Limit to 60 FPS

        self.db_manager.close()
        pygame.quit()
        self.logger.info("Game closed.")

    def handle_selection(self, selection):
        if self.current_view == self.menu_view:
            if selection == "Start Game":
                self.logger.info("Starting a new game...")
                # Initialize or reset game state here
                # For example, create default teams, leagues, etc.
                self.current_view = self.team_view
            elif selection == "Load Game":
                self.logger.info("Loading game...")
                # Implement load game functionality
                self.current_view = self.team_view  # Example transition
            elif selection == "Settings":
                self.logger.info("Opening settings...")
                self.current_view = self.settings_view
            elif selection == "Exit":
                self.logger.info("Exiting game...")
                self.running = False
        elif self.current_view == self.settings_view:
            if selection == "Back to Main Menu":
                self.logger.info("Returning to main menu from settings.")
                self.current_view = self.menu_view
            elif selection == "Controls":
                self.logger.info("Opening controls settings.")
                self.settings_controller.display_controls()
            elif selection == "Apply Settings":
                self.logger.info("Applying settings.")
                self.settings_controller.apply_settings()
        elif self.current_view == self.team_view:
            if selection == "Back to Main Menu":
                self.logger.info("Returning to main menu from team management.")
                self.current_view = self.menu_view
            elif selection == "Manage Formation":
                self.logger.info("Managing team formation.")
                # Implement formation management
                self.logger.info("Team formation management not yet implemented.")
            elif selection == "Manage Tactics":
                self.logger.info("Managing team tactics.")
                # Implement tactics management
                self.logger.info("Team tactics management not yet implemented.")
            elif selection == "View Players":
                self.logger.info("Viewing team players.")
                self.current_view = self.player_view
        elif self.current_view == self.player_view:
            if selection == "Back to Team Menu":
                self.logger.info("Returning to team management from player view.")
                self.current_view = self.team_view
            elif selection == "View Player Details":
                self.logger.info("Viewing player details.")
                # Implement player details viewing
                self.logger.info("Player details viewing not yet implemented.")
            elif selection == "Update Player Skills":
                self.logger.info("Updating player skills.")
                # Implement updating player skills
                self.logger.info("Player skills updating not yet implemented.")
            elif selection == "Update Player Morale":
                self.logger.info("Updating player morale.")
                # Implement updating player morale
                self.logger.info("Player morale updating not yet implemented.")
            elif selection == "Update Player Contract":
                self.logger.info("Updating player contract.")
                # Implement updating player contract
                self.logger.info("Player contract updating not yet implemented.")
        elif self.current_view == self.match_view:
            if selection == "Back to Main Menu":
                self.logger.info("Returning to main menu from match view.")
                self.current_view = self.menu_view
            elif selection == "View Match Details":
                self.logger.info("Viewing match details.")
                # Implement match details viewing
                self.logger.info("Match details viewing not yet implemented.")
            elif selection == "Simulate Match":
                self.logger.info("Simulating a match.")
                # Implement match simulation
                self.logger.info("Match simulation not yet implemented.")
            elif selection == "Delete Match":
                self.logger.info("Deleting a match.")
                # Implement match deletion
                self.logger.info("Match deletion not yet implemented.")
        elif self.current_view == self.league_view:
            if selection == "Back to Main Menu":
                self.logger.info("Returning to main menu from league view.")
                self.current_view = self.menu_view
            elif selection == "View Standings":
                self.logger.info("Viewing league standings.")
                # Implement standings viewing
                self.logger.info("League standings viewing not yet implemented.")
            elif selection == "View Fixtures":
                self.logger.info("Viewing league fixtures.")
                # Implement fixtures viewing
                self.logger.info("League fixtures viewing not yet implemented.")
            elif selection == "View Statistics":
                self.logger.info("Viewing league statistics.")
                # Implement statistics viewing
                self.logger.info("League statistics viewing not yet implemented.")
        elif self.current_view == self.finance_view:
            if selection == "Back to Main Menu":
                self.logger.info("Returning to main menu from finance view.")
                self.current_view = self.menu_view
            elif selection == "View Budget":
                self.logger.info("Viewing team budget.")
                # Implement budget viewing
                self.logger.info("Budget viewing not yet implemented.")
            elif selection == "View Revenue":
                self.logger.info("Viewing team revenue.")
                # Implement revenue viewing
                self.logger.info("Revenue viewing not yet implemented.")
            elif selection == "View Expenses":
                self.logger.info("Viewing team expenses.")
                # Implement expenses viewing
                self.logger.info("Expenses viewing not yet implemented.")
            elif selection == "Update Budget":
                self.logger.info("Updating team budget.")
                # Implement budget updating
                self.logger.info("Budget updating not yet implemented.")
        elif self.current_view == self.transfer_view:
            if selection == "Back to Main Menu":
                self.logger.info("Returning to main menu from transfer view.")
                self.current_view = self.menu_view
            elif selection == "Buy Player":
                self.logger.info("Initiating player purchase.")
                # Implement player buying functionality
                self.logger.info("Player purchase not yet implemented.")
            elif selection == "Sell Player":
                self.logger.info("Initiating player sale.")
                # Implement player selling functionality
                self.logger.info("Player sale not yet implemented.")
        else:
            self.logger.warning(f"Unhandled selection: {selection}")

    def update(self):
        # Update game state if needed
        pass

    def render(self):
        # Render the current view
        try:
            if isinstance(self.current_view, MenuView):
                self.current_view.display_menu()
            elif isinstance(self.current_view, TeamView):
                # Example: Display first team; in practice, manage selected team
                teams = self.team_controller.db_manager.get_all_teams()
                if teams:
                    team = Team(
                        name=teams[0]['name'],
                        formation=teams[0]['formation'],
                        tactics=teams[0]['tactics']
                    )
                    team.id = teams[0]['id']
                    self.team_view.display_team(team)
            elif isinstance(self.current_view, PlayerView):
                # Example: Display all players
                players = self.player_controller.db_manager.get_all_players()
                player_objects = [Player(
                    name=p['name'],
                    position=p['position'],
                    skills=p['skills'],
                    morale=p['morale'],
                    contract_end=p['contract_end']
                ) for p in players]
                for player, p in zip(player_objects, players):
                    player.id = p['id']
                self.player_view.display_players(player_objects)
            elif isinstance(self.current_view, MatchView):
                # Example: Display all matches
                matches = self.match_controller.db_manager.get_all_matches()
                match_objects = [Match(
                    home_team=match['home_team_id'],
                    away_team=match['away_team_id'],
                    date=match['date'],
                    home_score=match['home_score'],
                    away_score=match['away_score']
                ) for match in matches]
                for match, m in zip(match_objects, matches):
                    match.id = m['id']
                self.match_view.display_matches(match_objects)
            elif isinstance(self.current_view, LeagueView):
                # Example: Display all leagues
                leagues = self.league_controller.db_manager.get_all_leagues()
                league_objects = [League(
                    name=league['name'],
                    season=league['season']
                ) for league in leagues]
                for league, l in zip(league_objects, leagues):
                    league.id = l['id']
                self.league_view.display_leagues(league_objects)
            elif isinstance(self.current_view, FinanceView):
                # Example: Display finance for first team
                finances = self.finance_controller.db_manager.get_all_finances()
                if finances:
                    finance = finances[0]
                    self.finance_view.display_finances(finance)
            elif isinstance(self.current_view, SettingsView):
                # Display current settings
                self.settings_view.display_settings()
            elif isinstance(self.current_view, TransferView):
                # Example: List available players and teams
                available_players = self.transfer_controller.list_available_players()
                teams = self.team_controller.db_manager.get_all_teams()
                self.transfer_view.display_transfers(available_players, teams)
            else:
                self.logger.warning(f"No render method defined for view: {self.current_view}")
        except Exception as e:
            self.logger.error(f"Error rendering view: {e}")

if __name__ == '__main__':
    game = GameController()
    game.start_game()
