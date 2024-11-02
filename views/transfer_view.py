import pygame

class TransferView:
    def __init__(self, screen):
        self.screen = screen
        try:
            self.font = pygame.font.Font('assets/fonts/c64_font.ttf', 24)
        except FileNotFoundError:
            self.font = pygame.font.SysFont('Arial', 24)
            print("Custom font not found. Using default font.")
        self.menu_options = ["Back to Main Menu", "Buy Player", "Sell Player"]
        self.selected_index = 0
        self.available_players = []
        self.teams = []
        self.selected_player = None

    def display_transfers(self, available_players, teams):
        self.available_players = available_players
        self.teams = teams
        self.screen.fill((0, 0, 0))  # Clear screen with black
        y_offset = 50

        # Display Transfers Title
        title = self.font.render("Player Transfers", True, (255, 255, 255))
        self.screen.blit(title, (400 - title.get_width() // 2, y_offset))
        y_offset += 40

        # Display Available Players
        available_title = self.font.render("Available Players:", True, (255, 255, 255))
        self.screen.blit(available_title, (50, y_offset))
        y_offset += 30
        for i, player in enumerate(self.available_players):
            player_info = f"{player.id}: {player.name} - {player.position}"
            text = self.font.render(player_info, True, (255, 255, 255))
            text_rect = text.get_rect(topleft=(50, y_offset + i * 25))
            self.screen.blit(text, text_rect)
        y_offset += len(self.available_players) * 25 + 20

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
            elif event.key == pygame.K_RETURN:
                return self.menu_options[self.selected_index]
        return None
