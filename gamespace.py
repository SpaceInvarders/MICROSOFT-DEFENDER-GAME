import pygame
import os
import time
import random

# Instrucciones y contexto del Juego MICROSOFT DEFENDER SERVER
# Contexto: Tu eres el antivirus windows defender, y tu deber es protejer el servidor.
# No es una tarea facil, ya que vas a recibir constantes ataques informaticos (Malwares, Adware, Spyware, Ransomware, Troyano... etc).
# Pero, tu poderoso sistema de eliminaci[on de virus, erradica los virus, los intentos de hackeo y el intento de bajar el server.
# Miles de personas usan este servidor. Debes de tener bastante cuidado, puesto que algunos virus pueden destreuirte. Cabe reclacar que,
# todos estos virus tienen el fin de dañar el servidor, y algunos traen una mascara de red social, debes tener cuidado!!!.
# Instruciones: Bueno como les selañaba antes, deben protejer el servidor, con W, A, S, D las teclas tradicionales, para mover el jugador en videojuegos.
# Y con la tecla SPACE, podran disparar el rayo que desintegra a los viurus. SUERTE ANTIVIRUS!!!
pygame.font.init()

WIDTH, HEIGHT = 600, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MICROSOFT DEFENDER SERVER")
# Load Images
aware = pygame.transform.scale(pygame.image.load(os.path.join("asets/aware_icon.png")), (60, 60))
biohazard = pygame.transform.scale(pygame.image.load(os.path.join("asets/Biohazard_symbol.png")), (60, 60))
brand = pygame.transform.scale(pygame.image.load(os.path.join("asets/brand_icon.png")), (60, 60))
discord = pygame.transform.scale(pygame.image.load(os.path.join("asets/discord_logo.png")), (60, 60))
facebook = pygame.transform.scale(pygame.image.load(os.path.join("asets/facebook_icon.png")), (60, 60))
gus = pygame.transform.scale(pygame.image.load(os.path.join("asets/gus_icon.png")), (60, 60))
gusano = pygame.transform.scale(pygame.image.load(os.path.join("asets/Gusano_icon.png")), (60, 60))
instagram = pygame.transform.scale(pygame.image.load(os.path.join("asets/instagram_icon.png")), (60, 60))
microsoft = pygame.transform.scale(pygame.image.load(os.path.join("asets/Microsoft_Defender_icon.png")), (60, 120))
phishing = pygame.transform.scale(pygame.image.load(os.path.join("asets/phishing_icon.png")), (60, 60))
reddit = pygame.transform.scale(pygame.image.load(os.path.join("asets/reddit_icon.png")), (60, 60))
ranso = pygame.transform.scale(pygame.image.load(os.path.join("asets/ranso_icon.png")), (60, 60))
spy = pygame.transform.scale(pygame.image.load(os.path.join("asets/Spy-icon.png")), (60, 60))
trojan = pygame.transform.scale(pygame.image.load(os.path.join("asets/trojan-horse.png")), (60, 60))
twitter_icon = pygame.transform.scale(pygame.image.load(os.path.join("asets/twitter_icon.png")), (60, 60))
whatsapp = pygame.transform.scale(pygame.image.load(os.path.join("asets/Whatsapp-Icon.png")), (60, 60))

# Lasers
RED_LASER = pygame.image.load(os.path.join("asets/pixel_laser_red.png"))
BLUE_LASER = pygame.image.load(os.path.join("asets/pixel_laser_blue.png"))
GREEN_LASER = pygame.image.load(os.path.join("asets/pixel_laser_green.png"))
YELLOW_LASER = pygame.image.load(os.path.join("asets/pixel_laser_yellow.png"))

# Cargar Fondo
BG = pygame.transform.scale(pygame.image.load(os.path.join("asets/fondocyber.jpg")), (WIDTH, HEIGHT))


class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not (self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)


class Ship:
    COOLDOWN = 30

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = microsoft
        self.laser_img = BLUE_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0),
                         (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (
        self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health / self.max_health),
        10))


class Enemy(Ship):
    COLOR_MAP = {
        "red1": (aware, RED_LASER),
        "red2": (biohazard, RED_LASER),
        "red3": (brand, RED_LASER),
        "green1": (gus, GREEN_LASER),
        "green2": (gusano, GREEN_LASER),
        "green3": (phishing, GREEN_LASER),
        "yellow1": (trojan, YELLOW_LASER),
        "yellow2": (ranso, YELLOW_LASER),
        "yellow3": (spy, YELLOW_LASER),
        "blue1": (instagram, BLUE_LASER),
        "blue2": (whatsapp, BLUE_LASER),
        "blue3": (facebook, BLUE_LASER)

    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x - 20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None  # (x, y)

def main():
    run = True
    FPS = 60
    level = 1
    lives = 5
    main_font = pygame.font.SysFont("Sans-Serif", 45)
    lost_font = pygame.font.SysFont("Sans-Serif", 65)

    enemies = []
    wave_length = 5
    enemy_vel = 1

    player_vel = 5
    laser_vel = 7

    player = Player(300, 630)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    def redraw_window():
        WIN.blit(BG, (0, 0))
        # draw text
        lives_label = main_font.render(f"lives: {lives}", 1, (255, 255, 255))
        level_label = main_font.render(f"level: {level}", 1, (255, 255, 255))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        if lost:
            lost_label = lost_font.render("YOU HAVE BEEN HACKED!!", 1, (255, 255, 255))
            WIN.blit(lost_label, (WIDTH / 2 - lost_label.get_width() / 2, 350))

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100), random.choice(
                    ["red1", "red2", "red3", "green1", "green2", "green3", "yellow1", "yellow2", "yellow3", "blue1",
                     "blue2", "blue3"]))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0:  # left
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH:  # right
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0:  # up
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 15 < HEIGHT:  # down
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            if random.randrange(0, 2 * 60) != 1:
                pass
            else:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        player.move_lasers(-laser_vel, enemies)

def main_menu():
    title_font = pygame.font.SysFont("Sans-Serif", 65)
    run = True
    while run:
        WIN.blit(BG, (0, 0))
        title_label = title_font.render("Press The mouse", 1, (255, 255, 255))
        WIN.blit(title_label, (WIDTH / 2 - title_label.get_width() / 2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type != pygame.MOUSEBUTTONDOWN:
                continue
            main()
    pygame.quit()


main_menu()
