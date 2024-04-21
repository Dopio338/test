from pygame import *
from random import randint


window = display.set_mode((700,500))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'), (700, 500))

clock = time.Clock()
speed = 5


#mixer.init()
#mixer.music.load('space.ogg')
#mixer.music.play()
#fire = mixer.Sound('fire.ogg')

lost = 0
font.init()
font1 = font.Font(None, 36)
font2 = font.Font(None, 36)



class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_speed, player_x, player_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (150,150))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.direction = 'left'
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < 595:
            self.rect.x += self.speed 
        if keys_pressed[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys_pressed[K_s] and self.rect.y < 395:
            self.rect.y += self.speed
    def fire(self):
        bullet = Bullet('bullet2.png', 8, self.rect.x, self.rect.y)
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= 500:
            self.rect.y = -100
            lost = lost  + 1


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()

bullets = sprite.Group()
monsters = sprite.Group()
asteroids = sprite.Group()
for i in range(5):
    monster = Enemy('enemy2.png', randint(2,8), randint(0, 500), -100)
    monsters.add(monster) 
    asteroid = Enemy('asteroid.png', randint(1,5), randint(1,5), -100)
    asteroids.add(asteroid)


player = Player('rocket2.png', 5, 350, 350)

y1 = 0
y2 = -500
game = True
kills = 0
finish = False

while game:
    collides = sprite.groupcollide(monsters, bullets, True, True)
    for i in collides:
        kills += 1
        monster = Enemy('enemy2.png', randint(2,8), randint(0, 500), -100)
        monsters.add(monster) 
        text_win = font2.render('YOU WIN:' , True, (255, 255, 255))
 
        
    
        

    window.blit(background, (0,y1))
    window.blit(background, (0,y2))
    text_loose = font1.render(
    'Пропущено:' + str(lost), True, (255, 255, 255)
    
)
    text_kills = font1.render(
    'Счёт:' + str(kills), True, (255, 255, 255)
    
)
    text_win = font1.render(
    'YOU WIN!', True, (255, 255, 255)
    
)
    window.blit(text_kills,(10,40))
    window.blit(text_loose,(10,10))  
    y1 += 5
    y2 += 5
    if y1 >= 500:
        y1 = -500
    if y2 >= 500:
        y2 = -500
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()
    if finish != True:
        if kills >= 10:
            window.blit(text_win,(10,10))
            finish = True
        player.reset()
        player.update()
        monsters.draw(window)
        monsters.update()  
        bullets.update()
        bullets.draw(window)
        asteroids.draw(window)
        asteroids.update()    
        clock.tick(60)
        display.update()
