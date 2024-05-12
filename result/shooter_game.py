from pygame import *
from random import randint
lost = 0
score = 0

font.init()
font1 = font.SysFont('Arial', 40)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))

#hard
#goal = 99
#norm
#goal = 40
#ez
goal = 10
max_lost = 10
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Maze")
background = transform.scale(image.load("pppppppppppppp.jpg"), (win_width, win_height))

clock = time.Clock()
FPS = 60

mixer.init()
mixer.music.load('ads.wav')
mixer.music.play()
fire_sound = mixer.Sound('fire1.ogg')

font.init()
font2 = font.SysFont('Arial', 40)


class GameSprite(sprite.Sprite):
    #конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
           self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
           self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)




class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_height - 80)
            self.rect.y = 0
            self.speed = randint(1, 2)
            lost = lost + 1

class Bullet(GameSprite):
    def update(self): 
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

logo_5ka = Player('logo_5ka.png', 5, win_height - 100, 80, 100, 10 )

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy('ahan.png', randint(80, win_width - 80), - 40, 80, 50, randint(1, 2))
    monsters.add(monster)

bullets = sprite.Group()

finish = False
run = True

asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Enemy("magnit.png", randint(80, win_width - 80), - 40, 80, 50, randint(1, 2))
    asteroids.add(asteroid)

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                logo_5ka.fire()
    if not finish:
        window.blit(background,(0, 0))
        text = font2.render('Счёт:' + str(score), 1,(0, 255, 0))
        window.blit(text, (10, 20))
        text_lose = font2.render('Ты бульба:' + str(lost), 1,(212, 119, 26))
        window.blit(text_lose, (10, 50))
        logo_5ka.update()
        monsters.update()
        bullets.update()
        asteroid.update()

        logo_5ka.reset()
        monsters.draw(window)
        asteroids.draw(window)
        bullets.draw(window)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy('ahan.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        if sprite.spritecollide(logo_5ka, monsters, False) or lost >= max_lost:
            finish = True 
            window.blit(lose, (200, 200))

        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        display.update()
    else:
        score = 0
        lost = 0
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
    
    display.update()
    clock.tick(FPS)