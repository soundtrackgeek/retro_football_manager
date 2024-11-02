from database.db_manager import DatabaseManager
from views.settings_view import SettingsView
from utils.logger import setup_logger

class SettingsController:
    def __init__(self, db_manager: DatabaseManager, settings_view: SettingsView):
        self.db_manager = db_manager
        self.settings_view = settings_view
        self.logger = setup_logger('settings_controller_logger', 'logs/settings_controller.log')

    def handle_settings(self):
        """
        Handle the settings menu loop.
        """
        running = True
        while running:
            selected_option = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                selected_option = self.settings_view.handle_input(event)

            if selected_option:
                self.handle_menu_selection(selected_option)

            self.settings_view.display_settings()
            pygame.display.flip()

    def handle_menu_selection(self, selection):
        self.logger.info(f"Settings menu selection: {selection}")
        if selection == "Back to Main Menu":
            self.logger.info("Returning to main menu from settings.")
            return "Back to Main Menu"
        elif selection.startswith("Difficulty"):
            self.logger.info("Difficulty setting adjusted.")
            # Difficulty is already adjusted in SettingsView
            pass
        elif selection.startswith("Audio"):
            self.logger.info("Audio setting adjusted.")
            # Audio is already adjusted in SettingsView
            pass
        elif selection == "Controls":
            self.logger.info("Opening controls settings.")
            self.display_controls()
        elif selection == "Apply Settings":
            self.logger.info("Applying settings.")
            self.apply_settings()

    def display_controls(self):
        """
        Display and manage control settings.
        """
        # Placeholder for controls settings
        # Implement controls display and adjustment as needed
        self.logger.info("Displaying controls settings...")
        print("Controls settings are not yet implemented.")

    def apply_settings(self):
        """
        Apply and save settings.
        """
        try:
            difficulty = self.settings_view.difficulty_levels[self.settings_view.current_difficulty]
            audio = self.settings_view.audio_settings[self.settings_view.current_audio]
            self.db_manager.set_setting('difficulty', difficulty)
            self.db_manager.set_setting('audio', audio)
            self.logger.info(f"Settings applied: Difficulty={difficulty}, Audio={audio}")
            print("Settings have been applied successfully.")
        except Exception as e:
            self.logger.error(f"Error applying settings: {e}")
            print("An error occurred while applying settings.")
