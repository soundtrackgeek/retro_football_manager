import pygame

class TeamView:
    def __init__(self, screen):
        self.screen = screen
        try:
            self.font = pygame.font.Font('assets/fonts/c64_font.ttf', 24)
        except FileNotFoundError:
            self.font = pygame.font.SysFont('Arial', 24)
            print("Custom font not found. Using default font.")
        self.team_info = {}
        self.menu_options = ["Back to Main Menu", "Manage Formation", "Manage Tactics", "View Players"]
        self.selected_index = 0

    def display_team(self, team):
        self.screen.fill((0, 0, 0))  # Clear screen with black
        y_offset = 50

        # Display Team Name
        title = self.font.render(f"Team: {team.name}", True, (255, 255, 255))
        self.screen.blit(title, (400 - title.get_width() // 2, y_offset))
        y_offset += 40

        # Display Formation
        formation = self.font.render(f"Formation: {team.formation}", True, (255, 255, 255))
        self.screen.blit(formation, (400 - formation.get_width() // 2, y_offset))
        y_offset += 30

        # Display Tactics
        tactics = self.font.render(f"Tactics: {team.tactics}", True, (255, 255, 255))
        self.screen.blit(tactics, (400 - tactics.get_width() // 2, y_offset))
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
            elif event.key == pygame.K_RETURN:
                return self.menu_options[self.selected_index]
        return None
