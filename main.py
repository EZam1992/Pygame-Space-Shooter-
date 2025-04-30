import pygame 
from os.path import join 
from random import randint, uniform

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('space shooter', 'images', 'player.png')).convert_alpha()
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2))
        self.player_direction = pygame.math.Vector2()
        self.player_speed = 300

        #cooldown 
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400

    def laser_timer(self): 
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True
            
    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.player_direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.player_direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.player_direction = self.player_direction.normalize() if self.player_direction else self.player_direction
        self.rect.center += self.player_direction * self.player_speed * dt
        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser(laser_surf, self.rect.midtop, (all_sprites, laser_sprites))
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
        self.laser_timer()

class Star(pygame.sprite.Sprite):
    def __init__(self, star_surf, *groups):
        super().__init__(*groups)
        self.image = star_surf
        self.rect = self.image.get_frect(center = (randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)))

class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, *groups):
        super().__init__(*groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)

    def update(self, dt):
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0:
            self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, pos, *groups):
        super().__init__(*groups)
        self.original_surf = surf
        self.image = self.original_surf
        self.rect = self.image.get_frect(center = pos)
        self.start_time = pygame.time.get_ticks()
        self.lifetime = 3000 
        self.direction = pygame.Vector2(uniform(-0.5, 0.5), 1)
        self.speed = randint(400, 500)
        self.mask = pygame.mask.from_surface(self.image)
        self.rotation_speed = randint(0, 100)
        self.rotation = 0

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()

        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.original_surf, self.rotation, 1)
        self.rect = self.image.get_frect(center = self.rect.center)

def collision():

    global running

    sprite_collision = pygame.sprite.spritecollide(player, meteor_sprites, True, pygame.sprite.collide_mask)
    if sprite_collision:
        running = False
    
    for laser in laser_sprites:
        collided_sprite = pygame.sprite.spritecollide(laser, meteor_sprites, True)
        if collided_sprite:
            laser.kill()

def display_score():
    current_time = pygame.time.get_ticks() / 100
    font_surface = font.render(str(int(current_time)), True, (240, 240, 240))
    font_rect = font_surface.get_frect(midbottom = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50))
    display_surface.blit(font_surface, font_rect)
    pygame.draw.rect(display_surface, (240, 240, 240), font_rect.inflate(20, 10).move(0, -6), 6, 1)
#general setup 
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Shooter")

# variables needed for game logistics
running = True 
clock = pygame.time.Clock()

#create sprite groups
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()

#imports
star_surf = pygame.image.load(join('space shooter', 'images', 'star.png')).convert_alpha()
laser_surf = pygame.image.load(join('space shooter', 'images', 'laser.png')).convert_alpha()
meteor_surf = pygame.image.load(join('space shooter', 'images', 'meteor.png')).convert_alpha()
font = pygame.font.Font(join('space shooter', 'images', 'Oxanium-Bold.ttf'), 40)


#sprite generation
for i in range(20):
    Star(star_surf, all_sprites)
player = Player(all_sprites)

# custom events -> meteor event 
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 200)



while running:
    dt = clock.tick() / 1000
    # event loop 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
        if event.type == meteor_event:
            x, y = randint(0, WINDOW_WIDTH), randint(-200, -100)
            Meteor(meteor_surf, (x, y), (all_sprites, meteor_sprites))

    #update
    all_sprites.update(dt)
    collision()

    #draw the game 
    display_surface.fill('#3a2e3f')
    display_score()
    all_sprites.draw(display_surface)
    
    pygame.display.update()


pygame.quit()
