import pygame

class SettingsView:
    def __init__(self, screen):
        self.screen = screen
        try:
            self.font = pygame.font.Font('assets/fonts/c64_font.ttf', 24)
        except FileNotFoundError:
            self.font = pygame.font.SysFont('Arial', 24)
            print("Custom font not found. Using default font.")
        self.menu_options = ["Back to Main Menu", "Difficulty: Easy", "Audio: On", "Controls", "Apply Settings"]
        self.selected_index = 0
        self.difficulty_levels = ["Easy", "Medium", "Hard"]
        self.audio_settings = ["On", "Off"]
        self.current_difficulty = 0  # Index of difficulty_levels
        self.current_audio = 0       # Index of audio_settings

    def display_settings(self):
        self.screen.fill((0, 0, 0))  # Clear screen with black
        y_offset = 50

        # Display Settings Title
        title = self.font.render("Settings", True, (255, 255, 255))
        self.screen.blit(title, (400 - title.get_width() // 2, y_offset))
        y_offset += 40

        # Display Current Settings
        difficulty = self.font.render(f"Difficulty: {self.difficulty_levels[self.current_difficulty]}", True, (255, 255, 255))
        audio = self.font.render(f"Audio: {self.audio_settings[self.current_audio]}", True, (255, 255, 255))
        controls = self.font.render("Controls: WASD or Arrow Keys", True, (255, 255, 255))

        self.screen.blit(difficulty, (400 - difficulty.get_width() // 2, y_offset))
        y_offset += 30
        self.screen.blit(audio, (400 - audio.get_width() // 2, y_offset))
        y_offset += 30
        self.screen.blit(controls, (400 - controls.get_width() // 2, y_offset))
        y_offset += 50

        # Display Menu Options
        for i, option in enumerate(self.menu_options):
            if i == self.selected_index:
                color = (255, 255, 255)  # White for selected
            else:
                color = (100, 100, 100)  # Gray for others
            text = self.font.render(option, True, color)
            text_rect = text.get_rect(center=(400, y_offset + i * 40))
            self.screen.blit(text, text_rect)

        pygame.display.flip()

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.menu_options)
            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.menu_options)
            elif event.key == pygame.K_LEFT:
                self.adjust_setting(-1)
            elif event.key == pygame.K_RIGHT:
                self.adjust_setting(1)
            elif event.key == pygame.K_RETURN:
                return self.menu_options[self.selected_index]
        return None

    def adjust_setting(self, direction):
        # Adjust Difficulty
        if self.selected_index == 1:
            self.current_difficulty = (self.current_difficulty + direction) % len(self.difficulty_levels)
            self.menu_options[1] = f"Difficulty: {self.difficulty_levels[self.current_difficulty]}"
        # Adjust Audio
        elif self.selected_index == 2:
            self.current_audio = (self.current_audio + direction) % len(self.audio_settings)
            self.menu_options[2] = f"Audio: {self.audio_settings[self.current_audio]}"
