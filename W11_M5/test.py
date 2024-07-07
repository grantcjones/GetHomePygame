import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Initialize Music
pygame.mixer.music.load("8-bit-space-123218.mp3")
pygame.mixer.music.play(-1)

# Initialize sound effects
missile_out = pygame.mixer.Sound("missile_launch.mp3")
missile_hit = pygame.mixer.Sound("explosion_short.mp3")
player_death = pygame.mixer.Sound("death_sound.mp3")
enemy_death = pygame.mixer.Sound("8-bit-fireball.mp3")

# Define colors
BACKGROUND = (53, 81, 92)
WHITE = (255, 255, 255)
PLAYER = "player.png"

# Set up the display
screen = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption('Get Home')

# Initialize font
font = pygame.font.Font(None, 36)

# Initialize Entity classes
class Player(pygame.sprite.Sprite):
    def __init__(self, player_image):
        super().__init__()
        self.image = pygame.image.load(player_image)
        self.rect = self.image.get_rect()
        self.rect.topleft = (500, 690)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, image: str):
        super().__init__()
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        enemy_x = random.randint(0, 960)
        self.rect.topleft = (enemy_x, -100)
        self.y_velocity = 0

    def update(self):
        self.y_velocity += 0.2    # Incremental movement
        if self.y_velocity >= 1:
            self.rect.y += 1  # Apply movement
            self.y_velocity -= 1  # Reset the velocity counter
        if self.rect.top > 1000:
            self.kill()

class StrongEnemy(Enemy):
    def __init__(self, image: str):
        super().__init__(image)
        self.health = 3  # StrongEnemy requires 2 hits to be defeated

    def hit(self):
        self.health -= 1

    def update(self):
        super().update()

class Missile(pygame.sprite.Sprite):
    def __init__(self, frame_0: str, x, y):
        super().__init__()
        self.image = pygame.image.load(frame_0)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    
    def update(self):
        self.rect.y -= 1
        if self.rect.bottom < 0:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, frames: list, death_x, death_y):
        super().__init__()
        self.frames = [pygame.image.load(frame) for frame in frames]
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (death_x, death_y)
        self.animation_timer = 0
        self.animation_speed = 85  # Adjust this value to control the speed of animation

    def update(self):
        # Update animation timer
        self.animation_timer += 1

        # Check if it's time to switch to the next frame
        if self.animation_timer >= self.animation_speed:
            self.current_frame += 1
            if self.current_frame < len(self.frames):
                self.image = self.frames[self.current_frame]
            else:
                self.kill()  # Remove the sprite once the animation is done
            self.animation_timer = 0

def play_cutscene():
    cutscene_images = [PLAYER]
    cutscene_text1 = ["Ok Rooster, you've completed your objective, time to head home..."]
    cutscene_text2 = ["wait, multiple bogeys converging on your location, punch a hole"]
    cutscene_text3 = ["and get back to the carrier!"]
    cutscene_duration = [7000]  # Duration in milliseconds for each part of the cutscene

    for i in range(len(cutscene_images)):
        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time < cutscene_duration[i]:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            screen.fill(BACKGROUND)  # Clear screen
            image = pygame.image.load(cutscene_images[i])
            screen.blit(image, (500, 690))  # Draw the current image
            text_surface1 = font.render(cutscene_text1[i], True, WHITE)
            text_surface2 = font.render(cutscene_text2[i], True, WHITE)
            text_surface3 = font.render(cutscene_text3[i], True, WHITE)

            screen.blit(text_surface1, (50, 10))  # Draw the current text
            screen.blit(text_surface2, (50, 30))
            screen.blit(text_surface3, (50, 50))
            
            pygame.display.flip()
            pygame.time.wait(10)  # Small delay to prevent high CPU usage

# Initialize player
player = Player(PLAYER)

# Load enemy sprite
enemies = pygame.sprite.Group()
strong_enemies = pygame.sprite.Group()
missiles = pygame.sprite.Group()
explosions = pygame.sprite.Group()

# Timer for enemy spawning
enemy_spawn_timer = 0
enemy_spawn_interval = 200

strong_enemy_spawn_timer = 0
strong_enemy_interval = 450

# Flag for missile firing
can_fire_missile = True
alt = True

# Load game over image
game_over_image = pygame.image.load("game_over.png")
game_over_rect = game_over_image.get_rect(center=(500, 500))

# Score
score = 0

# Play the cutscene before the game starts
play_cutscene()

# Main game loop
running = True
game_over = False
game_over_start_time = None

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if not game_over:
                if event.key == pygame.K_SPACE and can_fire_missile:
                    if alt:
                        missile = Missile("missile.png", player.rect.centerx - 10, player.rect.top)
                        missile_out.play()
                        alt = False
                    else:
                        missile = Missile("missile.png", player.rect.centerx + 5, player.rect.top)
                        missile_out.play()
                        alt = True
                    missiles.add(missile)
                    can_fire_missile = False  # Disable firing until key is released
            else:
                # If game over, any key except ESC will restart the game
                if event.key == pygame.K_e:
                    # Restart the game
                    player.rect.topleft = (500, 690)
                    enemies.empty()
                    strong_enemies.empty()
                    missiles.empty()
                    explosions.empty()
                    score = 0
                    game_over = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                can_fire_missile = True  # Enable firing again when key is released

    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.rect.left > 0:
            player.rect.x -= 1
        if keys[pygame.K_d] and player.rect.right < 1000:
            player.rect.x += 0.5
        if keys[pygame.K_w] and player.rect.top > 100:
            player.rect.y -= 1
        if keys[pygame.K_s] and player.rect.bottom < 980:
            player.rect.y += 0.5

        # Update enemy spawn timer
        enemy_spawn_timer += 1
        if enemy_spawn_timer >= enemy_spawn_interval:
            enemy_spawn_timer = 0
            if random.random() > 0.8:
                strong_enemy = StrongEnemy("strong_enemy.png")
                strong_enemies.add(strong_enemy)
            else:
                enemy = Enemy("enemy.png")
                enemies.add(enemy)

        strong_enemies.update()
        enemies.update()
        missiles.update()

        # Collision detection
        if pygame.sprite.spritecollideany(player, enemies):
            game_over_start_time = pygame.time.get_ticks()
            player_death.play()
            explosion = Explosion(["explosion_frame1.png", "explosion_frame2.png", "explosion_frame3.png"], player.rect.centerx, player.rect.centery)
            explosions.add(explosion)
            game_over = True

        if pygame.sprite.spritecollideany(player, strong_enemies):
            game_over_start_time = pygame.time.get_ticks()
            player_death.play()
            explosion = Explosion(["explosion_frame1.png", "explosion_frame2.png", "explosion_frame3.png"], player.rect.centerx, player.rect.centery)
            explosions.add(explosion)
            game_over = True

        enemy_hits = pygame.sprite.groupcollide(missiles, enemies, True, True)
        for hit in enemy_hits:
            missile_hit.play()
            score += 10  # Increase score
            explosion = Explosion(["explosion_frame1.png", "explosion_frame2.png", "explosion_frame3.png"], hit.rect.centerx, hit.rect.centery)
            explosions.add(explosion)

        strong_enemy_hits = pygame.sprite.groupcollide(strong_enemies, missiles, False, True)
        for strong_enemy in strong_enemy_hits:
            missile_hit.play()
            strong_enemy.health -= 1
            if strong_enemy.health <= 0:
                enemy_death.play()
                strong_enemy.kill()
                score += 20  # Increase score for strong enemy
                explosion = Explosion(["large_explosion_frame1.png", "large_explosion_frame2.png", "large_explosion_frame3.png"], strong_enemy.rect.centerx, strong_enemy.rect.centery)
                explosions.add(explosion)
            else:
                explosion = Explosion(["explosion_frame1.png", "explosion_frame2.png", "explosion_frame3.png"], missile.rect.centerx, missile.rect.centery)
                explosions.add(explosion)

        explosions.update()

    # Drawing
    screen.fill(BACKGROUND)  # Clear the screen before drawing
    if not game_over:
        enemies.draw(screen)
        strong_enemies.draw(screen)
        missiles.draw(screen)
        explosions.draw(screen)
        screen.blit(player.image, player.rect)

        # Render the score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        controls_text = font.render(f"W: UP, A: LEFT, S: DOWN, D: RIGHT, SPACE: Fire Missile", True, WHITE)
        screen.blit(controls_text, (10, 950))

    else:
        current_time = pygame.time.get_ticks()
        if current_time - game_over_start_time >= 1000:
            screen.blit(game_over_image, game_over_rect)
            score_text = font.render(f"Score: {score}", True, WHITE)
            screen.blit(score_text, (10, 10))
        else:
            explosions.draw(screen)
            explosions.update()

    pygame.display.flip()

pygame.quit()