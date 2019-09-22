import pygame
from settings import *
from gameobject import *


class Tank():
    def __init__(self, x, y, speed, size, dx=0.0, dy=0.0):
        self.x = x
        self.y = y
        self.speed = speed
        self.dx = dx
        self.dy = dy
        self.size = size
        self.angle = 0

    def draw(self, game_display, img, camera):
        t = pygame.transform.rotate(img, self.angle+270)
        game_display.blit(t, camera.follow(self))

    def draw_explosion(self, game_display, camera):
        img = pygame.image.load('images/Explosion.png')
        second = pygame.image.load('images/exp_1.png')
        third = pygame.image.load('images/exp_2.png')
        images = []
        images.append(img)
        images.append(second)
        images.append(third)
        for image in images:
            game_display.blit(image, camera.follow(self))


class Player(Tank):
    def __init__(self, x, y, speed, size, hp, items=None, value = 0):
        Tank.__init__(self, x, y, speed, size)
        self.items = {
            'first': None,
            'second': None,
            'third': None,
            'fourth': None,
            'fifth': None,
            'sixth': None}
        self.hp = hp
        self.missiles = []
        self.angle = 0
        self.logical_a = 0
        self.gold = 600
        self.value = value
        self.data = {
            'x': 50,
            'y': 50,
            'destroyed' : Terrain(0,0, 0, 'water'),
            'hp': 100,
            'missiles': [],
            'angle': 0,
            'speed': 3,
            'gold': 600
        }
        self.destroyed_object = Terrain(0,0, 0, 'water')


    def modify(self, game_display, camera, PLAYER_SPRITE):
        if not inside_boundaries(self):
            self.dx = 0
            self.dy = 0
        self.x += self.dx
        self.y += self.dy

        self.data['x'] = self.x
        self.data['y'] = self.y
        self.data['angle'] = self.angle
        self.data['gold'] = self.gold
        self.data['hp'] = self.hp
        self.data['missiles'] = self.missiles

        
        self.draw(game_display, PLAYER_SPRITE, camera)
        self.dx = 0.0
        self.dy = 0.0
        self.logical_a = 0

    def bullet_check(self):
        for bullet in self.missiles:
            if bullet.x > 0 and bullet.y > 0:
                bullet.x += bullet.velocity_x
                bullet.y += bullet.velocity_y
            else:
                self.missiles.pop(self.missiles.index(bullet))

class Enemy(Tank):
    def __init__(self, x, y, size, kind, hp=100, img=None, missiles=[]):
        self.hp = hp
        if kind == 'regular':
            self.img = pygame.image.load('images/ally.png')
            self.speed = 1
        elif kind == 'fast':
            self.img = pygame.image.load('images/enemy_fast.png')
            self.speed = 2
        elif kind == 'heavy':
            self.img = pygame.image.load('images/enemy_heavy.png')
            self.speed = 0.5
            self.hp = 200
        Tank.__init__(self, x, y, self.speed, size)
        self.hp = hp
        self.missiles = missiles

    def make_move(self, obj):
        direction = ''
        if self.y > obj.y:
            self.dy -= self.speed
            self.dx = 0
            direction = 'up'
        elif self.y < obj.y:
            self.dy += self.speed
            self.dx = 0
            direction = 'down'
        elif self.x > obj.x:
            self.dx -= self.speed
            self.dy = 0
            direction = 'right'
        elif self.x < obj.x:
            self.dx += self.speed
            self.dy = 0
            direction = 'left'
        return direction

    def shoot(self, enemy, direction):
        for bullet in self.missiles:
            if bullet.x > 0 and bullet.y > 0:
                bullet.x += bullet.velocity_x
                bullet.y += bullet.velocity_y
            else:
                self.missiles.pop(self.missiles.index(bullet))
        tdirection_x = 0
        tdirection_y = 0
        if (abs(enemy.x - self.x) < OBJ_SIZE or
           abs(enemy.y - self.y) < OBJ_SIZE):
            tdirection_x = 0
            tdirection_y = 0
            if direction == "right":
                tdirection_x = -1
                tdirection_y = 0
            elif direction == "left":
                tdirection_x = 1
                tdirection_y = 0
            elif direction == "up":
                tdirection_x = 0
                tdirection_y = -1
            elif direction == "down":
                tdirection_x = 0
                tdirection_y = 1
            missile_e = Missile(self.x, self.y, 2, tdirection_x, tdirection_y)
            if len(self.missiles) < 1:
                self.missiles.append(missile_e)

    def modify(self, game_display, camera):
        self.x += self.dx
        self.y += self.dy
        self.draw(game_display, self.img, camera)
        self.dx = 0
        self.dy = 0

def inside_boundaries(object):
    return object.x + object.dx > 0 \
    and object.x < DISPLAY_WIDTH*2 \
    and object.y + object.dy > 0 \
    and object.y < DISPLAY_HEIGHT*2
