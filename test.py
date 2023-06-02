import pygame
pygame.init()

# Set up the window
WIDTH = 640
HEIGHT = 480
win = pygame.display.set_mode((WIDTH, HEIGHT))

# Set up the font
FONT_SIZE = 10
font = pygame.font.SysFont('Arial', FONT_SIZE)

# Set up the text
text = "This is a long text that can be scrolled by the user." * 10
text_surface = font.render(text, True, (255, 255, 255))

# Set up the scrolling
scroll_speed = 5
scroll_pos = 0

# Set up the scrolling buttons
UP_ARROW = pygame.K_SPACE
DOWN_ARROW = pygame.K_DOWN

# Start the game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == UP_ARROW:
                scroll_pos += scroll_speed
            elif event.key == DOWN_ARROW:
                scroll_pos -= scroll_speed

    # Constrain the scroll position to the text surface bounds
    scroll_pos = min(scroll_pos, 0)
    scroll_pos = max(scroll_pos, -(text_surface.get_height() - HEIGHT))

    # Draw the text to the window
    win.fill((0, 0, 0))
    win.blit(text_surface, (0, scroll_pos))

    # Update the display
    pygame.display.update()