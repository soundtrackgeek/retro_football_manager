# utils/helpers.py

def load_font(font_path, size):
    """
    Load a font from the specified path.
    If the font is not found, load the default font.
    """
    try:
        return pygame.font.Font(font_path, size)
    except FileNotFoundError:
        print("Custom font not found. Using default font.")
        return pygame.font.SysFont('Arial', size)

def render_text(text, font, color=(255, 255, 255)):
    """
    Render text using the specified font and color.
    """
    return font.render(text, True, color)

def get_center_position(screen, surface):
    """
    Get the position to center a surface on the screen.
    """
    screen_rect = screen.get_rect()
    surface_rect = surface.get_rect()
    return (screen_rect.width // 2 - surface_rect.width // 2,
            screen_rect.height // 2 - surface_rect.height // 2)
