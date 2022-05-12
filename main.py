from re import T
from tkinter import Widget
import pygame, control
from random import randint

WIDTH = 1000
HEIGHT = 650
FPS = 90
YELLOW = (166, 168, 8)
Y_B = (173, 216, 230)
W_WW = (227, 160, 25)

class Car(pygame.sprite.Sprite):
    def __init__(self, WIDTH, HEIGHT, size, path):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(self.image,(size, size))
        self.rect = self.image.get_rect(bottomright=(WIDTH + 400, HEIGHT + 80))
        self.x = self.rect.x
        self.y = self.rect.y
        self.WIDTH = WIDTH

    def update_car(self):
        self.x -= 1

class Wheels(Car):
    def __init__(self, WIDTH, HEIGHT, size, path):
        super().__init__(WIDTH, HEIGHT, size, path)
        self.image_up = self.image
        self.image_right = pygame.transform.rotate(self.image, -90)
        self.image_down = pygame.transform.flip(self.image, 0, 1)
        self.image_left = pygame.transform.rotate(self.image, 90)
        self.array = [self.image_up, self.image_right, self.image_down, self.image_left]
        

class Human(pygame.sprite.Sprite):
    def __init__(self, WIDTH, HEIGHT, size, path):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(self.image,(size, size))
        self.rect = self.image.get_rect(center=(WIDTH / 2 - 60, HEIGHT / 4 + 350))
        self.start_pos = self.rect.x
        self.WIDTH = WIDTH
    
    def update_human(self):
        self.rect.x -= 1
    
    def return_human(self):
        if self.rect.x != self.start_pos:
            self.rect.x += 1

def draw_sun():
    pygame.draw.circle(screen, YELLOW, (80, 60), 50)

def draw_clouds(start_x):
    pygame.draw.circle(screen, W_WW, (start_x + 90, 125), 48)
    pygame.draw.circle(screen, W_WW, (start_x + 130, 120), 40)
    pygame.draw.circle(screen, W_WW, (start_x + 50, 130), 30)
    pygame.draw.circle(screen, W_WW, (start_x + 170, 130), 25)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ZOOOOOOMBIES")
clock = pygame.time.Clock()
background = pygame.image.load("./img/background.png").convert()
background = pygame.transform.scale(background,(WIDTH,HEIGHT))

def main():    
    car = Car(WIDTH, HEIGHT, 400, './img/car.png')
    wheel1 = Wheels(WIDTH - 243, HEIGHT - 130, 100, './img/wheel.png')
    wheel2 = Wheels(WIDTH - 25, HEIGHT - 130, 100, './img/wheel.png')
    human = Human(WIDTH, HEIGHT, 200, './img/human.png')

    cstart = randint(0, 600)
    cstart1 = randint(200, 600)
    flag_human = True
    flag_change = True
    i = 0
    while True:
        control.events()
        screen.blit(background, [0,0])
        
        draw_clouds(cstart)
        draw_clouds(cstart1)
        draw_sun()

        cstart -= 1
        cstart1 -= 1
        if cstart <= -250:
            cstart = WIDTH + 200
        if cstart1 <= -250:
            cstart1 = WIDTH + 200

        # Отрисовка машины 
        screen.blit(car.image, (car.x, car.y))

        # Отрисовка колес
        screen.blit(wheel1.array[i], (wheel1.x, wheel1.y))
        screen.blit(wheel2.array[i], (wheel2.x, wheel2.y))
        
        # Выход человека
        if car.x != WIDTH / 4:
            i += 1
            if i >= 3:
                i = 0
            car.update_car()
            wheel1.update_car()
            wheel2.update_car()
        else:
            screen.blit(human.image, human.rect)
            if human.rect.x >= -400 and flag_human:
                human.update_human()
            else:
                flag_human = False
                if flag_change:
                    human.image = pygame.transform.flip(human.image, 1, 0)
                    flag_change = False
                human.return_human()
        
                # будет солнце
                # затем он выбежит, за ним будет гнаться зомби, сядет в машину, собьет зомби и уедеет и так заново

        if human.rect.x == human.start_pos:
            car.update_car()
            wheel1.update_car()
            wheel2.update_car()

        if car.x <= -400:
            car.x = WIDTH + 400
            wheel1.x = WIDTH + 457
            wheel2.x = WIDTH + 676
            human.image = pygame.transform.flip(human.image, 1, 0)
            flag_change = True
            flag_human = True

        pygame.display.update() 
        clock.tick(FPS)

if __name__ == '__main__':
    main()