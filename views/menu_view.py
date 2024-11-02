import pygame

class MenuView:
    def __init__(self, screen):
        self.screen = screen
        self.options = ["Start Game", "Settings", "Exit"]
        self.selected_index = 0
        self.font = pygame.font.Font(None, 36)

    def draw(self):
        self.screen.fill((0, 0, 0))
        
        # Draw title
        title = self.font.render("Retro Football Manager", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.screen.get_width() // 2, 50))
        self.screen.blit(title, title_rect)

        # Draw menu options
        y_position = 150
        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected_index else (255, 255, 255)
            text = self.font.render(option, True, color)
            text_rect = text.get_rect(center=(self.screen.get_width() // 2, y_position))
            self.screen.blit(text, text_rect)
            y_position += 50

        pygame.display.flip()

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                return self.options[self.selected_index]
        return None

    def on_start_game(self):
        # ...existing code...
        db_manager.initialize_english_teams()
        # ...existing code...
