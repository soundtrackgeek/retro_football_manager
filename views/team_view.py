import pygame

class TeamView:
    def __init__(self, screen):
        self.screen = screen
        try:
            self.font = pygame.font.Font('assets/fonts/c64_font.ttf', 24)
        except FileNotFoundError:
            self.font = pygame.font.SysFont('Arial', 24)
            print("Custom font not found. Using default font.")
        self.menu_options = ["Back to Main Menu", "Manage Formation", "Manage Tactics", "View Players"]
        self.selected_index = 0
        self.team = None
        self.available_formations = ["4-4-2", "3-5-2", "4-3-3", "3-4-3"]
        self.available_tactics = ["Offensive", "Defensive", "Balanced"]
        self.selected_option = None
        self.current_menu = "team_menu"  # Add this line

    def display_team(self, team):
        self.team = team
        self.current_menu = "team_menu"  # Add this line
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

    def display_formation_menu(self):
        formation_menu_options = self.available_formations + ["Cancel"]
        self.menu_options = formation_menu_options
        self.selected_index = 0
        self.screen.fill((0, 0, 0))  # Clear screen with black
        y_offset = 100

        # Display Formation Menu Title
        title = self.font.render("Select New Formation", True, (255, 255, 255))
        self.screen.blit(title, (400 - title.get_width() // 2, y_offset))
        y_offset += 40

        # Display Formation Options
        for i, option in enumerate(formation_menu_options):
            if i == self.selected_index:
                color = (255, 255, 255)  # White for selected
            else:
                color = (100, 100, 100)  # Gray for others
            text = self.font.render(option, True, color)
            text_rect = text.get_rect(center=(400, y_offset + i * 30))
            self.screen.blit(text, text_rect)
        pygame.display.flip()

    def display_tactics_menu(self):
        tactics_menu_options = self.available_tactics + ["Cancel"]
        self.menu_options = tactics_menu_options
        self.selected_index = 0
        self.screen.fill((0, 0, 0))  # Clear screen with black
        y_offset = 100

        # Display Tactics Menu Title
        title = self.font.render("Select New Tactics", True, (255, 255, 255))
        self.screen.blit(title, (400 - title.get_width() // 2, y_offset))
        y_offset += 40

        # Display Tactics Options
        for i, option in enumerate(tactics_menu_options):
            if i == self.selected_index:
                color = (255, 255, 255)  # White for selected
            else:
                color = (100, 100, 100)  # Gray for others
            text = self.font.render(option, True, color)
            text_rect = text.get_rect(center=(400, y_offset + i * 30))
            self.screen.blit(text, text_rect)
        pygame.display.flip()

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.menu_options)
            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.menu_options)
            elif event.key == pygame.K_RETURN:
                selected_option = self.menu_options[self.selected_index]
                if self.current_menu == "team_menu":
                    return selected_option
                elif self.current_menu == "formation_menu":
                    if selected_option != "Cancel":
                        return f"Change Formation to {selected_option}"
                    else:
                        self.menu_options = ["Back to Main Menu", "Manage Formation", "Manage Tactics", "View Players"]
                        self.selected_index = 0
                        self.display_team(self.team)
                        return None
                elif self.current_menu == "tactics_menu":
                    if selected_option != "Cancel":
                        return f"Change Tactics to {selected_option}"
                    else:
                        self.menu_options = ["Back to Main Menu", "Manage Formation", "Manage Tactics", "View Players"]
                        self.selected_index = 0
                        self.display_team(self.team)
                        return None
            elif event.key == pygame.K_ESCAPE:
                # Handle escape key to go back
                if self.current_menu in ["formation_menu", "tactics_menu"]:
                    self.menu_options = ["Back to Main Menu", "Manage Formation", "Manage Tactics", "View Players"]
                    self.selected_index = 0
                    self.display_team(self.team)
                return None
        return None

    def manage_formation(self):
        self.current_menu = "formation_menu"
        self.display_formation_menu()

    def manage_tactics(self):
        self.current_menu = "tactics_menu"
        self.display_tactics_menu()

    def set_menu_option(self, option):
        if option.startswith("Change Formation to "):
            new_formation = option.replace("Change Formation to ", "")
            self.team.formation = new_formation
            # Logic to update the team formation in the database should be handled by the controller
        elif option.startswith("Change Tactics to "):
            new_tactics = option.replace("Change Tactics to ", "")
            self.team.tactics = new_tactics
            # Logic to update the team tactics in the database should be handled by the controller

    def set_current_menu(self, menu):
        self.current_menu = menu

    def display_empty_state(self):
        """Display when no teams are available"""
        # Clear the screen
        self.screen.fill((0, 0, 0))
        
        # Render text
        font = pygame.font.Font(None, 36)
        text = font.render("No teams available", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.screen.get_width()/2, self.screen.get_height()/2))
        self.screen.blit(text, text_rect)
