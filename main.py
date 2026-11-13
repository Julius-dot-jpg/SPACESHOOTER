
import asyncio
import random
import pygame
import os

pygame.init()

# ==================================
# BILDSCHIRM
# ==================================
WIDTH = 1000
HEIGHT = 750

display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
DISPLAY_WIDTH, DISPLAY_HEIGHT = display.get_size()

screen = pygame.Surface((WIDTH, HEIGHT))
pygame.display.set_caption("SPACE SHOOTER")

clock = pygame.time.Clock()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# ==================================
# FARBEN
# ==================================
DARK = (5, 8, 25)
PANEL = (15, 25, 55)
WHITE = (245, 245, 255)
GREEN = (0, 230, 150)
RED = (255, 75, 90)
YELLOW = (255, 215, 70)
BLUE = (70, 160, 255)
PURPLE = (190, 100, 255)
ORANGE = (255, 150, 55)
CYAN = (70, 235, 255)


# ==================================
# SCHRIFTARTEN
# ==================================
font_big = pygame.font.Font(None, 90)
font_medium = pygame.font.Font(None, 55)
font_small = pygame.font.Font(None, 34)

# ==================================
# BILDER LADEN UND WEISS ENTFERNEN
# ==================================
def load_spaceship(path, size):
    full_path = os.path.join(BASE_DIR, path)

    image = pygame.image.load(full_path).convert_alpha()
    image = pygame.transform.scale(image, size)

    # Weiße Pixel transparent machen
    for x in range(image.get_width()):
        for y in range(image.get_height()):

            r, g, b, a = image.get_at((x, y))

            if r > 235 and g > 235 and b > 235:
                image.set_at((x, y), (255, 255, 255, 0))

    return image


# ==================================
# RAUMSCHIFFE LADEN
# ==================================
ship_images = {
    "Standardschiff": load_spaceship("assets/ship.png", (55, 60)),
    "Schiff 2": load_spaceship("assets/ship_1.png", (55, 60)),
    "Schiff 3": load_spaceship("assets/ship_2.png", (55, 60)),
    "Schiff 4": load_spaceship("assets/ship_3.png", (55, 60))
}

enemy_image = load_spaceship("assets/enemy.png", (50, 50))
enemy_image = pygame.transform.rotate(enemy_image, 180)


# ==================================
# HILFSFUNKTIONEN
# ==================================
def screen_position(pos):
    return (
        int(pos[0] * WIDTH / DISPLAY_WIDTH),
        int(pos[1] * HEIGHT / DISPLAY_HEIGHT)
    )


def draw_text(text, font, color, x, y):
    surface = font.render(str(text), True, color)
    rect = surface.get_rect(center=(x, y))
    screen.blit(surface, rect)


def button(text, x, y, width, height, color=PANEL):
    rect = pygame.Rect(x, y, width, height)

    pygame.draw.rect(
        screen, color, rect, border_radius=12
    )

    pygame.draw.rect(
        screen, CYAN, rect, 2, border_radius=12
    )

    draw_text(
        text, font_small, WHITE,
        x + width // 2, y + height // 2
    )

    return rect


# ==================================
# STERNE
# ==================================
def make_stars():
    return [
        [
            random.randrange(WIDTH),
            random.randrange(HEIGHT),
            random.choice([
                (100, 130, 180),
                (160, 190, 230),
                WHITE
            ]),
            random.choice([1, 1, 2])
        ]
        for _ in range(90)
    ]


stars = make_stars()


def draw_background():
    screen.fill(DARK)

    for star in stars:
        pygame.draw.circle(
            screen,
            star[2],
            (star[0], star[1]),
            star[3]
        )


def update_stars():
    for star in stars:
        star[1] += 1 + star[3]

        if star[1] >= HEIGHT:
            star[0] = random.randrange(WIDTH)
            star[1] = 0


# ==================================
# SPRACHEN
# ==================================
translations = {
    "Deutsch": {
        "title": "SPACE SHOOTER",
        "start": "Start",
        "settings": "Einstellungen",
        "shop": "Shop",
        "back": "Zurück",
        "score": "Punkte",
        "gameover": "SPIEL VORBEI",
        "restart": "Neustart",
        "menu": "Menü",
        "choose": "Sprache auswählen",
        "coins": "Münzen",
        "buy": "Kaufen",
        "owned": "Besitzt du",
        "equipped": "Ausgewählt",
        "health": "Leben",
        "fire": "FEUER"
    },

    "English": {
        "title": "SPACE SHOOTER",
        "start": "Start",
        "settings": "Settings",
        "shop": "Shop",
        "back": "Back",
        "score": "Score",
        "gameover": "GAME OVER",
        "restart": "Restart",
        "menu": "Menu",
        "choose": "Choose language",
        "coins": "Coins",
        "buy": "Buy",
        "owned": "Owned",
        "equipped": "Selected",
        "health": "Lives",
        "fire": "FIRE"
    },

    "Français": {
        "title": "SPACE SHOOTER",
        "start": "Démarrer",
        "settings": "Paramètres",
        "shop": "Boutique",
        "back": "Retour",
        "score": "Points",
        "gameover": "FIN DU JEU",
        "restart": "Rejouer",
        "menu": "Menu",
        "choose": "Choisir la langue",
        "coins": "Pièces",
        "buy": "Acheter",
        "owned": "Possédé",
        "equipped": "Choisi",
        "health": "Vies",
        "fire": "TIR"
    },

    "Español": {
        "title": "SPACE SHOOTER",
        "start": "Empezar",
        "settings": "Ajustes",
        "shop": "Tienda",
        "back": "Volver",
        "score": "Puntos",
        "gameover": "FIN DEL JUEGO",
        "restart": "Reiniciar",
        "menu": "Menú",
        "choose": "Elegir idioma",
        "coins": "Monedas",
        "buy": "Comprar",
        "owned": "Comprado",
        "equipped": "Elegido",
        "health": "Vidas",
        "fire": "DISPARAR"
    }
}

language = "Deutsch"


def tr(key):
    return translations[language][key]


# ==================================
# SHOP UND RAUMSCHIFFE
# ==================================
ships = {
    "Standardschiff": {"price": 0},
    "Schiff 2": {"price": 5},
    "Schiff 3": {"price": 10},
    "Schiff 4": {"price": 15}
}

owned_ships = ["Standardschiff"]
selected_ship = "Standardschiff"

coins = 0


# ==================================
# SPIELZUSTAND
# ==================================
state = "menu"

PLAYER_Y = HEIGHT - 145

player = pygame.Rect(
    WIDTH // 2 - 22,
    PLAYER_Y,
    44,
    48
)

player_speed = 8

bullets = []
enemies = []
particles = []

score = 0
lives = 3

last_shot = 0
last_enemy = 0
enemy_delay = 850

invulnerable_until = 0

moving_left = False
moving_right = False
shooting = False


def reset_movement():
    global moving_left, moving_right, shooting

    moving_left = False
    moving_right = False
    shooting = False


def reset_game():
    global player, bullets, enemies, particles
    global score, lives, last_shot, last_enemy
    global enemy_delay, invulnerable_until

    player = pygame.Rect(
        WIDTH // 2 - 22,
        PLAYER_Y,
        44,
        48
    )

    bullets = []
    enemies = []
    particles = []

    score = 0
    lives = 3

    last_shot = pygame.time.get_ticks()
    last_enemy = pygame.time.get_ticks()

    enemy_delay = 850
    invulnerable_until = 0

    reset_movement()


# ==================================
# GEGNER ERZEUGEN
# ==================================
def spawn_enemy():
    size = random.choice([34, 40, 46])

    x = random.randint(
        25,
        WIDTH - size - 25
    )

    rect = pygame.Rect(
        x,
        -size,
        size,
        size
    )

    enemies.append({
        "rect": rect,
        "speed": random.randint(2, 4)
                + min(score // 80, 4),
        "color": random.choice([
            RED, ORANGE, PURPLE
        ]),
        "hp": 2 if size >= 46 else 1
    })


# ==================================
# EXPLOSIONEN
# ==================================
def add_explosion(x, y, color):
    for _ in range(9):
        particles.append({
            "x": float(x),
            "y": float(y),
            "dx": random.uniform(-3, 3),
            "dy": random.uniform(-3, 3),
            "life": random.randint(12, 24),
            "color": color
        })


# ==================================
# SCHIESSEN
# ==================================
def shoot():
    global last_shot

    now = pygame.time.get_ticks()

    if now - last_shot >= 260:
        bullets.append(
            pygame.Rect(
                player.centerx - 4,
                player.top - 15,
                8,
                20
            )
        )

        last_shot = now


# ==================================
# TOUCH-STEUERUNG
# ==================================
def draw_controls():
    button("◀", 120, 650, 180, 75)
    button("▶", 320, 650, 180, 75)

    button(
        tr("fire"),
        700, 650, 180, 75,
        (45, 35, 65)
    )


def handle_touch(pos):
    global moving_left, moving_right, shooting

    if pygame.Rect(120, 650, 180, 75).collidepoint(pos):
        moving_left = True
        moving_right = False

    elif pygame.Rect(320, 650, 180, 75).collidepoint(pos):
        moving_right = True
        moving_left = False

    elif pygame.Rect(700, 650, 180, 75).collidepoint(pos):
        shooting = True
        shoot()


# ==================================
# SPIELLOGIK
# ==================================
def update_game():
    global score, coins, lives, state
    global last_enemy, enemy_delay
    global invulnerable_until

    keys = pygame.key.get_pressed()

    dx = int(
        keys[pygame.K_RIGHT] or keys[pygame.K_d]
    ) - int(
        keys[pygame.K_LEFT] or keys[pygame.K_a]
    )

    if moving_left:
        dx = -1

    elif moving_right:
        dx = 1

    # Nur seitliche Bewegung
    player.x += dx * player_speed

    player.y = PLAYER_Y
    player.clamp_ip(screen.get_rect())

    if keys[pygame.K_SPACE] or shooting:
        shoot()

    now = pygame.time.get_ticks()

    # Gegner erzeugen
    if now - last_enemy >= enemy_delay:
        spawn_enemy()

        last_enemy = now

        enemy_delay = max(
            300,
            850 - score * 3
        )

    # Projektile bewegen
    for bullet in bullets[:]:
        bullet.y -= 11

        if bullet.bottom < 0:
            bullets.remove(bullet)

    # Gegner bewegen
    for enemy in enemies[:]:
        enemy["rect"].y += enemy["speed"]

        if enemy["rect"].top > HEIGHT:
            enemies.remove(enemy)
            lives -= 1
            continue

        # Kollision mit Spieler
        if (
            enemy["rect"].colliderect(player)
            and now >= invulnerable_until
        ):
            enemies.remove(enemy)

            add_explosion(
                enemy["rect"].centerx,
                enemy["rect"].centery,
                enemy["color"]
            )

            lives -= 1
            invulnerable_until = now + 1100

    # Treffer durch Projektile
    for bullet in bullets[:]:
        hit = None

        for enemy in enemies:
            if bullet.colliderect(enemy["rect"]):
                hit = enemy
                break

        if hit:
            bullets.remove(bullet)

            hit["hp"] -= 1

            if hit["hp"] <= 0:
                enemies.remove(hit)

                score += 10
                coins += 1

                add_explosion(
                    hit["rect"].centerx,
                    hit["rect"].centery,
                    hit["color"]
                )

    # Partikel bewegen
    for particle in particles[:]:
        particle["x"] += particle["dx"]
        particle["y"] += particle["dy"]
        particle["life"] -= 1

        if particle["life"] <= 0:
            particles.remove(particle)

    if lives <= 0:
        state = "gameover"


# ==================================
# SPIEL ZEICHNEN
# ==================================
def draw_game():
    draw_background()

    draw_text(
        f"{tr('score')}: {score}",
        font_medium,
        WHITE,
        150,
        35
    )

    draw_text(
        f"{tr('health')}: {lives}",
        font_small,
        RED,
        825,
        35
    )

    # Spieler-Bitmap
    if (
        pygame.time.get_ticks() >= invulnerable_until
        or (pygame.time.get_ticks() // 100) % 2 == 0
    ):
        current_ship_image = ship_images[selected_ship]

        image_rect = current_ship_image.get_rect(
            center=player.center
)

        screen.blit(current_ship_image, image_rect)

    # Projektile
    for bullet in bullets:
        pygame.draw.rect(
            screen,
            CYAN,
            bullet,
            border_radius=4
        )

        pygame.draw.circle(
            screen,
            WHITE,
            bullet.midtop,
            4
        )

    # Gegner-Bitmap
    for enemy in enemies:
        enemy_rect = enemy_image.get_rect(
            center=enemy["rect"].center
        )

        screen.blit(enemy_image, enemy_rect)

        if enemy["hp"] > 1:
            pygame.draw.circle(
                screen,
                YELLOW,
                enemy["rect"].center,
                4
            )

    # Explosionen
    for particle in particles:
        pygame.draw.circle(
            screen,
            particle["color"],
            (int(particle["x"]), int(particle["y"])),
            max(1, particle["life"] // 6)
        )

    draw_controls()


# ==================================
# MENÜ
# ==================================
def draw_menu():
    draw_background()

    draw_text(
        tr("title"),
        font_big,
        CYAN,
        WIDTH // 2,
        170
    )

    pygame.draw.line(
        screen,
        CYAN,
        (280, 225),
        (720, 225),
        3
    )

    start = button(
        tr("start"),
        350, 300, 300, 75
    )

    settings = button(
        tr("settings"),
        350, 410, 300, 75
    )

    shop = button(
        tr("shop"),
        350, 520, 300, 75
    )

    draw_text(
        f"{tr('coins')}: {coins}",
        font_small,
        YELLOW,
        WIDTH // 2,
        680
    )

    return start, settings, shop


# ==================================
# EINSTELLUNGEN
# ==================================
def draw_settings():
    draw_background()

    draw_text(
        tr("settings"),
        font_big,
        CYAN,
        WIDTH // 2,
        120
    )

    draw_text(
        tr("choose"),
        font_medium,
        WHITE,
        WIDTH // 2,
        225
    )

    language_rects = []

    for i, lang in enumerate(translations):
        color = (
            (30, 75, 95)
            if language == lang else PANEL
        )

        rect = button(
            lang,
            350,
            275 + i * 82,
            300,
            60,
            color
        )

        language_rects.append((rect, lang))

    back = button(
        tr("back"),
        350, 635, 300, 60
    )

    return language_rects, back


# ==================================
# SHOP
# ==================================
def draw_shop():
    draw_background()

    draw_text(
        tr("shop"),
        font_big,
        CYAN,
        WIDTH // 2,
        85
    )

    draw_text(
        f"{tr('coins')}: {coins}",
        font_medium,
        YELLOW,
        WIDTH // 2,
        155
    )

    ship_rects = []

    for i, (name, data) in enumerate(ships.items()):
        y = 205 + i * 100

        rect = pygame.Rect(170, y, 660, 85)

        pygame.draw.rect(
            screen,
            PANEL,
            rect,
            border_radius=12
        )

        pygame.draw.rect(
            screen,
            CYAN if selected_ship == name else BLUE,
            rect,
            2,
            border_radius=12
        )

        # Raumschiff-Vorschau
        preview = pygame.transform.scale(
            ship_images[name],
            (55, 60)
        )

        screen.blit(preview, (195, y + 12))

        draw_text(
            name,
            font_medium,
            WHITE,
            430,
            y + 42
        )

        if name in owned_ships:
            status = (
                tr("equipped")
                if selected_ship == name
                else tr("owned")
            )
        else:
            status = f"{tr('buy')}: {data['price']}"

        draw_text(
            status,
            font_small,
            YELLOW,
            700,
            y + 42
        )

        ship_rects.append((rect, name))

    back = button(
        tr("back"),
        350, 635, 300, 60
    )

    return ship_rects, back


def shop_click(pos):
    global coins, selected_ship, state

    ship_rects, back = draw_shop()

    for rect, name in ship_rects:
        if rect.collidepoint(pos):

            price = ships[name]["price"]

            if name in owned_ships:
                selected_ship = name

            elif coins >= price:
                coins -= price
                owned_ships.append(name)
                selected_ship = name

    if back.collidepoint(pos):
        state = "menu"


# ==================================
# GAME OVER
# ==================================
def draw_end_screen():
    draw_background()

    draw_text(
        tr("gameover"),
        font_big,
        RED,
        WIDTH // 2,
        230
    )

    draw_text(
        f"{tr('score')}: {score}",
        font_medium,
        WHITE,
        WIDTH // 2,
        320
    )

    restart = button(
        tr("restart"),
        350, 410, 300, 70
    )

    menu = button(
        tr("menu"),
        350, 510, 300, 70
    )

    return restart, menu


# ==================================
# HAUPTPROGRAMM
# ==================================
async def main():
    global state, language
    global moving_left, moving_right, shooting

    reset_game()

    running = True

    while running:
        update_stars()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:

                    if state == "game":
                        state = "menu"
                        reset_movement()

                    else:
                        running = False

            # Tastatursteuerung
            if state == "game":

                if event.type == pygame.KEYUP:

                    if event.key in (
                        pygame.K_LEFT,
                        pygame.K_a
                    ):
                        moving_left = False

                    if event.key in (
                        pygame.K_RIGHT,
                        pygame.K_d
                    ):
                        moving_right = False

            # Handy- und Maussteuerung
            if state == "game":

                if event.type == pygame.MOUSEBUTTONDOWN:
                    handle_touch(
                        screen_position(event.pos)
                    )

                if event.type == pygame.MOUSEBUTTONUP:
                    reset_movement()

                if event.type == pygame.FINGERDOWN:
                    handle_touch((
                        int(event.x * WIDTH),
                        int(event.y * HEIGHT)
                    ))

                if event.type == pygame.FINGERUP:
                    reset_movement()

            # Menüs
            if event.type == pygame.MOUSEBUTTONDOWN:

                pos = screen_position(event.pos)

                if state == "menu":

                    start, settings, shop = draw_menu()

                    if start.collidepoint(pos):
                        reset_game()
                        state = "game"

                    elif settings.collidepoint(pos):
                        state = "settings"

                    elif shop.collidepoint(pos):
                        state = "shop"

                elif state == "settings":

                    language_rects, back = draw_settings()

                    for rect, lang in language_rects:
                        if rect.collidepoint(pos):
                            language = lang

                    if back.collidepoint(pos):
                        state = "menu"

                elif state == "shop":
                    shop_click(pos)

                elif state == "gameover":

                    restart, menu = draw_end_screen()

                    if restart.collidepoint(pos):
                        reset_game()
                        state = "game"

                    elif menu.collidepoint(pos):
                        state = "menu"

        if state == "game":
            update_game()

        if state == "menu":
            draw_menu()

        elif state == "settings":
            draw_settings()

        elif state == "shop":
            draw_shop()

        elif state == "game":
            draw_game()

        elif state == "gameover":
            draw_end_screen()

        display.fill(DARK)

        pygame.transform.scale(
            screen,
            (DISPLAY_WIDTH, DISPLAY_HEIGHT),
            display
        )

        pygame.display.flip()

        clock.tick(60)

        await asyncio.sleep(0)

    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())
