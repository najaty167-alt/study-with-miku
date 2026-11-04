
import pygame
import math
import sys

# ==================================================
# MIKU WORLD - PURE PYTHON / PYGAME
# ==================================================

pygame.init()

WIDTH, HEIGHT = 1100, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Miku World")

clock = pygame.time.Clock()

# Fonts
font = pygame.font.Font(None, 32)
small_font = pygame.font.Font(None, 24)
title_font = pygame.font.Font(None, 76)
subtitle_font = pygame.font.Font(None, 30)

# Colors
WHITE = (255, 255, 255)
AQUA = (20, 198, 216)
DARK_AQUA = (0, 155, 180)
LIGHT_AQUA = (125, 241, 245)
LAVENDER = (210, 190, 255)
PINK = (255, 150, 210)
RED = (255, 105, 130)
DARK_BLUE = (50, 95, 125)
GRAY = (115, 135, 150)
DARK_GRAY = (90, 110, 125)

current_page = "welcome"

# ==================================================
# HELPERS
# ==================================================

def draw_text(text, font_obj, color, x, y, center=True):
    image = font_obj.render(text, True, color)
    rect = image.get_rect()

    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)

    screen.blit(image, rect)


def draw_background():
    screen.fill(AQUA)

    # Diagonal stripes
    for offset in range(-HEIGHT, WIDTH, 75):
        pygame.draw.polygon(
            screen,
            DARK_AQUA,
            [
                (offset, 0),
                (offset + 30, 0),
                (offset + HEIGHT + 30, HEIGHT),
                (offset + HEIGHT, HEIGHT)
            ]
        )

    # Soft decorative circles
    pygame.draw.circle(screen, LIGHT_AQUA, (950, 100), 100, 3)
    pygame.draw.circle(screen, LAVENDER, (100, 610), 85, 3)
    pygame.draw.circle(screen, PINK, (990, 610), 50, 3)

    # Sparkles
    for x, y in [(180, 90), (900, 300), (800, 620), (300, 560)]:
        pygame.draw.line(screen, WHITE, (x - 10, y), (x + 10, y), 3)
        pygame.draw.line(screen, WHITE, (x, y - 10), (x, y + 10), 3)


def draw_button(text, rect, mouse_pos, accent=AQUA):
    hovered = rect.collidepoint(mouse_pos)

    # Hover enlargement
    if hovered:
        scale = 1.035
        draw_rect = pygame.Rect(
            rect.centerx - int(rect.width * scale / 2),
            rect.centery - int(rect.height * scale / 2),
            int(rect.width * scale),
            int(rect.height * scale)
        )
    else:
        draw_rect = rect.copy()

    # Button shadow
    shadow = draw_rect.move(0, 9)
    pygame.draw.polygon(
        screen,
        (65, 130, 150),
        [
            (shadow.left, shadow.top),
            (shadow.right - 28, shadow.top),
            (shadow.right, shadow.centery),
            (shadow.right - 28, shadow.bottom),
            (shadow.left, shadow.bottom),
            (shadow.left + 12, shadow.centery)
        ]
    )

    # Button face
    if hovered:
        face_color = accent
        text_color = WHITE
    else:
        face_color = (247, 253, 255)
        text_color = GRAY

    pygame.draw.polygon(
        screen,
        face_color,
        [
            (draw_rect.left, draw_rect.top),
            (draw_rect.right - 28, draw_rect.top),
            (draw_rect.right, draw_rect.centery),
            (draw_rect.right - 28, draw_rect.bottom),
            (draw_rect.left, draw_rect.bottom),
            (draw_rect.left + 12, draw_rect.centery)
        ]
    )

    # White border
    pygame.draw.polygon(
        screen,
        WHITE,
        [
            (draw_rect.left, draw_rect.top),
            (draw_rect.right - 28, draw_rect.top),
            (draw_rect.right, draw_rect.centery),
            (draw_rect.right - 28, draw_rect.bottom),
            (draw_rect.left, draw_rect.bottom),
            (draw_rect.left + 12, draw_rect.centery)
        ],
        3
    )

    # Arrow in its own separate area
    arrow_x = draw_rect.right - 42
    arrow_y = draw_rect.centery

    pygame.draw.polygon(
        screen,
        text_color,
        [
            (arrow_x - 7, arrow_y - 12),
            (arrow_x + 7, arrow_y),
            (arrow_x - 7, arrow_y + 12)
        ]
    )

    # Button text
    text_image = font.render(text, True, text_color)
    text_rect = text_image.get_rect(
        center=(draw_rect.centerx - 10, draw_rect.centery)
    )

    screen.blit(text_image, text_rect)

    return hovered


def draw_empty_miku_area():
    # Empty stage for Miku's future model
    stage = pygame.Rect(690, 100, 350, 500)

    pygame.draw.rect(
        screen,
        (80, 220, 235),
        stage,
        border_radius=35
    )

    pygame.draw.rect(
        screen,
        WHITE,
        stage,
        width=3,
        border_radius=35
    )

    # Decorative stars only - no character
    for x, y in [(760, 170), (950, 220), (850, 500)]:
        pygame.draw.line(screen, WHITE, (x - 10, y), (x + 10, y), 3)
        pygame.draw.line(screen, WHITE, (x, y - 10), (x, y + 10), 3)


def draw_footer():
    draw_text(
        "MIKU WORLD  -  STUDY WITH SPARKLE",
        small_font,
        WHITE,
        WIDTH // 2,
        HEIGHT - 28
    )


def draw_page_title(title):
    draw_text(title, title_font, WHITE, WIDTH // 2, 90)


def draw_back_button(mouse_pos):
    rect = pygame.Rect(35, HEIGHT - 90, 240, 55)

    draw_button("BACK TO MENU", rect, mouse_pos, PINK)

    return rect


# ==================================================
# WELCOME PAGE
# ==================================================

def draw_welcome(mouse_pos):
    draw_background()

    draw_text("MIKU WORLD", title_font, WHITE, 350, 105)
    draw_text(
        "YOUR MAGICAL STUDY ADVENTURE",
        subtitle_font,
        WHITE,
        350,
        165
    )

    # Welcome panel
    panel = pygame.Rect(100, 205, 510, 125)

    pygame.draw.rect(
        screen,
        (245, 253, 255),
        panel,
        border_radius=22
    )

    pygame.draw.rect(
        screen,
        WHITE,
        panel,
        width=3,
        border_radius=22
    )

    draw_text(
        "Welcome to Miku World!",
        font,
        DARK_BLUE,
        panel.centerx,
        panel.y + 35
    )

    draw_text(
        "Ready to begin your journey?",
        small_font,
        GRAY,
        panel.centerx,
        panel.y + 82
    )

    # Menu buttons - separate buttons, separate arrows
    buttons = [
        ("ENTER APP", pygame.Rect(100, 365, 510, 75), AQUA),
        ("ACHIEVEMENTS", pygame.Rect(100, 465, 245, 70), PINK),
        ("SETTINGS", pygame.Rect(365, 465, 245, 70), LAVENDER),
        ("CHANGE MIKU", pygame.Rect(100, 555, 510, 70), RED),
    ]

    for text, rect, color in buttons:
        draw_button(text, rect, mouse_pos, color)

    draw_empty_miku_area()
    draw_footer()

    return buttons


# ==================================================
# HOME PAGE
# ==================================================

def draw_home(mouse_pos):
    draw_background()

    draw_text("HELLO, STUDY STAR!", title_font, WHITE, WIDTH // 2, 100)
    draw_text(
        "Choose your next adventure",
        subtitle_font,
        WHITE,
        WIDTH // 2,
        155
    )

    buttons = [
        ("MY TASKS", pygame.Rect(100, 240, 400, 70), AQUA),
        ("ASK MIKU", pygame.Rect(100, 330, 400, 70), PINK),
        ("ACHIEVEMENTS", pygame.Rect(100, 420, 400, 70), LAVENDER),
        ("CUSTOMIZATION", pygame.Rect(100, 510, 400, 70), RED),
    ]

    for text, rect, color in buttons:
        draw_button(text, rect, mouse_pos, color)

    draw_empty_miku_area()
    draw_footer()

    return buttons


# ==================================================
# SIMPLE CONTENT PAGES
# ==================================================

def draw_content_page(page_name, mouse_pos):
    draw_background()
    draw_page_title(page_name)

    panel = pygame.Rect(170, 200, 760, 300)

    pygame.draw.rect(
        screen,
        (245, 253, 255),
        panel,
        border_radius=30
    )

    pygame.draw.rect(
        screen,
        WHITE,
        panel,
        width=3,
        border_radius=30
    )

    draw_text(
        page_name,
        title_font,
        DARK_BLUE,
        panel.centerx,
        panel.y + 85
    )

    draw_text(
        "This section is ready for your content!",
        small_font,
        GRAY,
        panel.centerx,
        panel.y + 165
    )

    back_rect = draw_back_button(mouse_pos)
    draw_footer()

    return [("BACK", back_rect, PINK)]


# ==================================================
# MAIN LOOP
# ==================================================

running = True

while running:

    mouse_pos = pygame.mouse.get_pos()
    clicked = False

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                clicked = True

    # Draw current page
    if current_page == "welcome":
        buttons = draw_welcome(mouse_pos)

    elif current_page == "home":
        buttons = draw_home(mouse_pos)

    else:
        buttons = draw_content_page(current_page, mouse_pos)

    # Handle clicks
    if clicked:

        for text, rect, color in buttons:

            if rect.collidepoint(mouse_pos):

                if text == "ENTER APP":
                    current_page = "home"

                elif text == "ACHIEVEMENTS":
                    current_page = "ACHIEVEMENTS"

                elif text == "SETTINGS":
                    current_page = "SETTINGS"

                elif text == "CHANGE MIKU":
                    current_page = "CHANGE MIKU"

                elif text == "MY TASKS":
                    current_page = "MY TASKS"

                elif text == "ASK MIKU":
                    current_page = "ASK MIKU"

                elif text == "CUSTOMIZATION":
                    current_page = "CUSTOMIZATION"

                elif text == "BACK":
                    current_page = "home"

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
