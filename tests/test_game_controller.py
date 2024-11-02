import unittest
from unittest.mock import MagicMock, patch
from controllers.game_controller import GameController
from controllers.team_controller import TeamController
from controllers.player_controller import PlayerController
from controllers.match_controller import MatchController
from controllers.league_controller import LeagueController
from controllers.finance_controller import FinanceController
from controllers.transfer_controller import TransferController
from controllers.settings_controller import SettingsController
from database.db_manager import DatabaseManager
from views.menu_view import MenuView
from views.team_view import TeamView
from views.player_view import PlayerView
from views.match_view import MatchView
from views.league_view import LeagueView
from views.finance_view import FinanceView
from views.settings_view import SettingsView
from views.transfer_view import TransferView

class TestGameController(unittest.TestCase):
    def setUp(self):
        # Mock the DatabaseManager
        self.db_manager = MagicMock(spec=DatabaseManager)
        
        # Initialize Controllers with mocked DatabaseManager
        self.team_controller = TeamController(self.db_manager)
        self.player_controller = PlayerController(self.db_manager)
        self.match_controller = MatchController(self.db_manager)
        self.league_controller = LeagueController(self.db_manager)
        self.finance_controller = FinanceController(self.db_manager)
        self.transfer_controller = TransferController(self.db_manager)
        self.settings_controller = SettingsController(self.db_manager, MagicMock(spec=SettingsView))
        
        # Initialize Views with mocked screen
        self.screen = MagicMock()
        self.menu_view = MenuView(self.screen)
        self.team_view = TeamView(self.screen)
        self.player_view = PlayerView(self.screen)
        self.match_view = MatchView(self.screen)
        self.league_view = LeagueView(self.screen)
        self.finance_view = FinanceView(self.screen)
        self.settings_view = SettingsView(self.screen)
        self.transfer_view = TransferView(self.screen)
        
        # Initialize GameController with mocked components
        self.game_controller = GameController()
        self.game_controller.db_manager = self.db_manager
        self.game_controller.team_controller = self.team_controller
        self.game_controller.player_controller = self.player_controller
        self.game_controller.match_controller = self.match_controller
        self.game_controller.league_controller = self.league_controller
        self.game_controller.finance_controller = self.finance_controller
        self.game_controller.transfer_controller = self.transfer_controller
        self.game_controller.settings_controller = self.settings_controller
        self.game_controller.menu_view = self.menu_view
        self.game_controller.team_view = self.team_view
        self.game_controller.player_view = self.player_view
        self.game_controller.match_view = self.match_view
        self.game_controller.league_view = self.league_view
        self.game_controller.finance_view = self.finance_view
        self.game_controller.settings_view = self.settings_view
        self.game_controller.transfer_view = self.transfer_view
        self.game_controller.logger = MagicMock()
        self.game_controller.current_view = self.menu_view

    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    def test_initialization(self, mock_clock, mock_set_caption, mock_set_mode):
        # Test if GameController initializes correctly
        self.assertIsNotNone(self.game_controller.screen)
        self.assertIsInstance(self.game_controller.clock, MagicMock)
        self.assertEqual(self.game_controller.current_view, self.menu_view)

    def test_handle_menu_selection_start_game(self):
        # Simulate selecting "Start Game" from the main menu
        self.game_controller.handle_selection("Start Game")
        self.assertEqual(self.game_controller.current_view, self.team_view)
        self.game_controller.logger.info.assert_any_call("Starting a new game...")

    def test_handle_menu_selection_load_game(self):
        # Simulate selecting "Load Game" from the main menu
        self.game_controller.handle_selection("Load Game")
        self.assertEqual(self.game_controller.current_view, self.team_view)
        self.game_controller.logger.info.assert_any_call("Loading game...")

    def test_handle_menu_selection_settings(self):
        # Simulate selecting "Settings" from the main menu
        self.game_controller.handle_selection("Settings")
        self.assertEqual(self.game_controller.current_view, self.settings_view)
        self.game_controller.logger.info.assert_any_call("Opening settings...")

    def test_handle_menu_selection_exit(self):
        # Simulate selecting "Exit" from the main menu
        with patch.object(self.game_controller, 'running', True):
            self.game_controller.handle_selection("Exit")
            self.assertFalse(self.game_controller.running)
            self.game_controller.logger.info.assert_any_call("Exiting game...")

    def test_handle_settings_back_to_main_menu(self):
        # Simulate returning to main menu from settings
        self.game_controller.current_view = self.settings_view
        self.game_controller.handle_selection("Back to Main Menu")
        self.assertEqual(self.game_controller.current_view, self.menu_view)
        self.game_controller.logger.info.assert_any_call("Returning to main menu from settings.")

    def test_handle_unknown_selection(self):
        # Simulate an unknown selection
        self.game_controller.handle_selection("Unknown Option")
        self.game_controller.logger.warning.assert_any_call("Unhandled selection: Unknown Option")

    def test_render_menu_view(self):
        # Test rendering the menu view
        self.game_controller.current_view = self.menu_view
        self.game_controller.render()
        self.menu_view.display_menu.assert_called_once()

    def test_render_team_view(self):
        # Mock team data
        team_data = [{'id': 1, 'name': 'Eagles FC', 'formation': '4-4-2', 'tactics': 'Offensive'}]
        self.db_manager.get_all_teams.return_value = team_data
        
        # Test rendering the team view
        self.game_controller.current_view = self.team_view
        self.game_controller.render()
        self.team_view.display_team.assert_called_once()

    def test_render_player_view(self):
        # Mock player data
        player_data = [
            {'id': 1, 'name': 'John Doe', 'position': 'Forward', 'skills': 85, 'morale': 90, 'contract_end': 2025},
            {'id': 2, 'name': 'Jane Smith', 'position': 'Midfielder', 'skills': 80, 'morale': 85, 'contract_end': 2024}
        ]
        self.db_manager.get_all_players.return_value = player_data
        
        # Test rendering the player view
        self.game_controller.current_view = self.player_view
        self.game_controller.render()
        self.player_view.display_players.assert_called_once()

    def test_render_match_view(self):
        # Mock match data
        match_data = [
            {'id': 1, 'home_team_id': 1, 'away_team_id': 2, 'date': '2024-05-15', 'home_score': 2, 'away_score': 1}
        ]
        self.db_manager.get_all_matches.return_value = match_data
        
        # Test rendering the match view
        self.game_controller.current_view = self.match_view
        self.game_controller.render()
        self.match_view.display_matches.assert_called_once()

    def test_render_league_view(self):
        # Mock league data
        league_data = [
            {'id': 1, 'name': 'Premier League', 'season': '2024/2025'}
        ]
        self.db_manager.get_all_leagues.return_value = league_data
        
        # Test rendering the league view
        self.game_controller.current_view = self.league_view
        self.game_controller.render()
        self.league_view.display_leagues.assert_called_once()

    def test_render_finance_view(self):
        # Mock finance data
        finance_data = {'id': 1, 'team_id': 1, 'budget': 1000000, 'revenue': 500000, 'expenses': 300000}
        self.db_manager.get_all_finances.return_value = [finance_data]
        
        # Test rendering the finance view
        self.game_controller.current_view = self.finance_view
        self.game_controller.render()
        self.finance_view.display_finances.assert_called_once_with(finance_data)

    def test_render_settings_view(self):
        # Test rendering the settings view
        self.game_controller.current_view = self.settings_view
        self.game_controller.render()
        self.settings_view.display_settings.assert_called_once()

    def test_render_transfer_view(self):
        # Mock available players and teams
        available_players = []
        teams = []
        self.transfer_controller.list_available_players.return_value = available_players
        self.team_controller.db_manager.get_all_teams.return_value = teams
        
        # Test rendering the transfer view
        self.game_controller.current_view = self.transfer_view
        self.game_controller.render()
        self.transfer_view.display_transfers.assert_called_once_with(available_players, teams)

if __name__ == '__main__':
    unittest.main()
