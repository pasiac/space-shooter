import random
import pygame
from models import ObserverSpritesGroup
# Global variables
from settings import background, WINDOW_HEIGHT, scrolling_speed, WINDOW_WIDTH, player_width, laser_img, laser_vel, \
    lasers, STATIC_DIR, asteroid_img, asteroid_width, big_asteroid_img, WHITE, PLAYER_VELOCITY, \
    DEFAULT_PLAYER_RECT_CENTER, player_img, FPS

enemies = ObserverSpritesGroup(pygame.sprite.Group())
all_sprites = ObserverSpritesGroup(pygame.sprite.Group())
kill_count = 0


# Models
class Background(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = background
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self):
        if self.rect.y > WINDOW_HEIGHT:
            self.rect.y = -WINDOW_HEIGHT
        else:
            self.rect.y += scrolling_speed


class BaseSpaceShip:
    def __init__(self, health, vel, cooldown, laser=None):
        self.health = health
        self.vel = vel
        self.laser = laser
        self.cooldown = cooldown


class BaseSprite(pygame.sprite.Sprite):
    def __init__(self, image, rect_center):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = rect_center


class PlayerSprite(BaseSprite):
    def __init__(self, spaceship: BaseSpaceShip, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.spaceship = spaceship
        self.last_laser_use = pygame.time.get_ticks()

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and self.rect.x < WINDOW_WIDTH - player_width:
            self.rect.x += self.spaceship.vel
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.spaceship.vel

        if keys[pygame.K_SPACE]:
            laser = LaserSprite(image=laser_img, rect_center=self.rect.center)
            self.last_laser_use = laser.shoot(self.last_laser_use)

        self._check_collision()

    def _check_collision(self):
        for enemy in enemies:
            if pygame.sprite.collide_rect(self, enemy):
                self.spaceship.health -= enemy.damage
                enemies.remove(enemy)
                all_sprites.remove(enemy)
                print("Hit sound")
                if self.spaceship.health < 1:
                    print("Game over")


class LaserSprite(BaseSprite):
    def __init__(self, attack=1, cooldown=300, uses_count=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attack = attack
        self.cooldown = cooldown
        self.uses_count = uses_count

    def update(self):
        self.rect.y -= laser_vel
        if self.rect.y < 0 or self.rect.y > WINDOW_HEIGHT:
            all_sprites.remove(self)
            lasers.remove(self)

    @staticmethod
    def play_fire_sound():
        pygame.mixer.Channel(0).play(
            pygame.mixer.Sound(f"{STATIC_DIR}/sounds/laser_sound.wav")
        )

    # doczytac o classmethods
    def shoot(self, last_used):
        now = pygame.time.get_ticks()
        if now - last_used >= self.cooldown:
            last_used = now
            self.play_fire_sound()
            lasers.append(self)
            all_sprites.add(self)
        return last_used


class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, width, health, velocity_x, velocity_y, damage):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (random.randrange(0, WINDOW_WIDTH - width), 0)
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.health = health
        self.damage = damage
        all_sprites.add(self)
        enemies.add(self)

    def update(self):
        global kill_count
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

        if self.rect.y > WINDOW_HEIGHT:
            self._remove_asteroid()
        # Hit mark
        for laser in lasers:
            if pygame.sprite.collide_rect(self, laser):
                laser_waste = self.health
                self.health -= laser.attack
                laser.attack -= laser_waste
                if laser.attack < 1:
                    lasers.remove(laser)
                    all_sprites.remove(laser)
                pygame.mixer.Channel(2).play(
                    pygame.mixer.Sound(f"{STATIC_DIR}/sounds/asteroid_explosion.wav")
                )
                if self.health < 1:
                    self._remove_asteroid()
                    kill_count += 1

    def _remove_asteroid(self):
        enemies.remove(self)
        all_sprites.remove(self)
        # play destroy sound


class EnemiesFactory:
    @staticmethod
    def get_enemy(enemy_type):
        if enemy_type == "asteroid":
            return Enemy(
                image=asteroid_img,
                width=asteroid_width,
                health=1,
                velocity_x=random.randrange(-1, 2),
                velocity_y=random.randrange(2, 5),
                damage=1,
            )
        elif enemy_type == "big asteroid":
            if kill_count > 20:
                return Enemy(
                    image=big_asteroid_img,
                    width=asteroid_width,
                    health=2,
                    velocity_x=random.randrange(-1, 2),
                    velocity_y=random.randrange(1, 3),
                    damage=1,
                )


def display_hud(player_health, screen):
    font = pygame.font.SysFont("Arial", 30)
    health = str(player_health)
    killed = str(kill_count)
    health_label = font.render('Health: ' + health, True, WHITE)
    screen.blit(health_label, (0, 0))
    killed_label = font.render('Points: ' + killed, True, WHITE)
    screen.blit(killed_label, (0, WINDOW_HEIGHT / 18))


# class GameState:
#     def __init__(self):
#         self.state =  'main_gameplay'
#
#     def main_gameplay(self):


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Space Shooter")
    pygame.mixer.pre_init(44100, -16, 1, 512)  # prevents sound delay
    clock = pygame.time.Clock()

    # Background
    all_sprites.add(Background((WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)))
    all_sprites.add(Background((WINDOW_WIDTH / 2, -WINDOW_HEIGHT / 2)))
    # Player spaceship
    player_spaceship = BaseSpaceShip(health=3, vel=PLAYER_VELOCITY, cooldown=200)
    player_sprite = PlayerSprite(
        image=player_img,
        rect_center=DEFAULT_PLAYER_RECT_CENTER,
        spaceship=player_spaceship,
    )
    all_sprites.add(player_sprite)

    enemies_factory = EnemiesFactory()

    while 1:
        clock.tick(FPS)
        all_sprites.draw(screen)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        # Spawn enemies
        if len(enemies) < 5:
            enemy = random.choices(["asteroid", "big asteroid"], [0.8, 0.2])
            enemies_factory.get_enemy(enemy_type=enemy[0])
        all_sprites.update()
        enemies.update()
        display_hud(player_health=player_sprite.spaceship.health, screen=screen)
        pygame.display.update()
        if player_sprite.spaceship.health < 1:
            pygame.mixer.Channel(3).play(pygame.mixer.Sound(f'{STATIC_DIR}/sounds/game_over.wav'))
            pygame.quit()
            return


if __name__ == "__main__":
    main()
