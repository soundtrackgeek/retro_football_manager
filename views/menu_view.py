import pygame

class MenuView:
    def __init__(self, screen):
        self.screen = screen
        try:
            self.font = pygame.font.Font('assets/fonts/c64_font.ttf', 32)
        except FileNotFoundError:
            self.font = pygame.font.SysFont('Arial', 32)
            print("Custom font not found. Using default font.")
        self.menu_options = ["Start Game", "Load Game", "Settings", "Exit"]
        self.selected_index = 0

    def display_menu(self):
        self.screen.fill((0, 0, 0))  # Clear screen with black
        for i, option in enumerate(self.menu_options):
            if i == self.selected_index:
                color = (255, 255, 255)  # White for selected
            else:
                color = (100, 100, 100)  # Gray for others
            text = self.font.render(option, True, color)
            text_rect = text.get_rect(center=(400, 200 + i * 60))
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
