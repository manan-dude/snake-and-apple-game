import pygame
import self as self
from pygame.locals import *  # this asterik will avail all the global variable from locals
import time
import random  #for moving the apples

SIZE = 40#  SIZE OF BLOCK IS 40 X 40.
Background_color= (255, 206, 207)

class Apple:
    def __init__(self,parent_screen):
        self.image = pygame.image.load("resources/apple.jpg").convert()
        self.parent_screen = parent_screen
        self.x= SIZE*3 # this should be in the multiple of 40 bcz we have to allign the apple and the snake
        self.y= SIZE*3
    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))  # blit function will draw apple on  the surface according to the  given ratio.
        pygame.display.flip()

    def move(self):
        self.x=random.randint(0,26)*SIZE# it should be the multiples of screen dimensions so it will move easily into the screen without going out.
        self.y=random.randint(0,17)*SIZE




class Snake:  # for  Snake-buliding through the help of blocks
    def __init__(self, parent_screen,length):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/block.jpg").convert()  # way to load an image
        # as the snake will grow we have to move all the accordingly to it so..
        self.x = [SIZE]*length  # WE HAVE BUILT AN FREE ARRAY
        self.y = [SIZE]*length
        self.direction = 'down'

    def increase_length(self): #all  the x and y holding blocks as an array so we have to increase its length
        self.length+=1
        self.x.append(-1)
        self.y.append(-1)

    def move_left(self):
        self.direction = 'left' # if the value of self.direction is left than it will pass to walk() fnt  and then the change is happen

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def draw(self):  # for drawing snake
          # if you don't write this code than the previous block with previous step also get printed.
        # WE HAVE TO DRAW THE NEW PART OF BLOCKS THAT BUILD THE SNAKE SO
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))  # blit function will draw block on  the surface according to the  given ratio.
        pygame.display.flip()

    def walk(self):# for changing the direction of moving snake

        for i in range(self.length-1,0,-1):# this loop is for assigning the value of previous block to reverse direction
             self.x[i] = self.x[i - 1]
             self.y[i] = self.y[i - 1]

        if self.direction == 'up':
                self.y[0] -= SIZE # here we are moving block in 40 dimension bcz it overlap the other block if taken minimum to 40.
        if self.direction == 'down':
            self.y[0] += SIZE
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE

        self.draw()



class Game:
    def __init__(self):  # we make class for making this code readable and generally main function dont have more line of codes
        pygame.init()  # it initiate the pygame module
        pygame.mixer.init()
        self.background_music()

        self.surface = pygame.display.set_mode((1080, 720))  # How much size you want,it initialize the window display

        self.render_background()  # for background colour,by adding self we are making it a class member
        # all this three lines are moved from main function to Game class.

        self.snake = Snake(self.surface,1)  # i created a snake in my Game(class) and (self.surface) is for assigning parent screen

        self.snake.draw()

        self.apple = Apple(self.surface)
        self.apple.draw()

    def is_collision(self,x1,y1,x2,y2):# made for the collision of apple and snake when coordinate of snake head collide with coordinate of
        if x1>=x2 and x1  < x2+SIZE:
            if y1>=y2 and y1  < y2+SIZE:
                return  True



    def play(self):# this the function which stay long with the event loop
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()  # for displaying score
        pygame.display.flip()

        #snake eating the  apple
        if self.is_collision(self.snake.x[0],self.snake.y[0],self.apple.x,self.apple.y):
            sound = pygame.mixer.Sound("resources/Apple-bite.mp3")
            pygame.mixer.Sound.play((sound))
            self.snake.increase_length()# here you want to inc the length of the snake during colision.
            self.apple.move()# when the snake head and apple collides we have to move apple at a random place


        # snake colliding with itself
        for i in range(3,self.snake.length):# here we take 3 because the head cant retake the position of 2nd and 3rd block .
            if self.is_collision(self.snake.x[0],self.snake.y[0],self.snake.x[i],self.snake.y[i]):
                sound1 = pygame.mixer.Sound("resources/1_snake_game_resources_crash.mp3")
                pygame.mixer.Sound.play(sound1)
                raise "Game over"# we try and exception for game over

    def show_game_over(self):
        #first we have to wipe out the screen
        self.render_background()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game is Over !, Your Score is :{self.snake.length}",True,(255,255,255))
        self.surface.blit(line1,(200,300))
        line2 = font.render("To play again press 'Enter' and for Exit press 'Esc'!",True,(255,255,255))
        self.surface.blit(line2 , (200,350))
        pygame.display.flip()
        pygame.mixer.music.pause()



    def reset(self):
        self.snake = Snake(self.surface,1)  # i created a snake in my Game(class) and (self.surface) is for assigning parent screen
        self.apple = Apple(self.surface)



    def display_score(self):
        font= pygame.font.SysFont('arial',30)
        score = font.render(f"Score:{self.snake.length}",True,(250,250,250)) # colour(200,200.200)
        self.surface.blit(score,(800,10))# we have a surface on which we shoe the screen and also mention the coordinates

    def background_music(self):
        pygame.mixer.music.load('resources/fm-freemusic-give-me-a-smile.mp3')
        pygame.mixer.music.play()

    def render_background(self):
        bg = pygame.image.load("resources/background.jpg")
        self.surface.blit(bg ,(0,0))

    def run(self):
        running = True  # as we are not using time module how we decide the screening of game window so we use event loops
        pause = False # for stopping the game

        while running:  # this will begin an infinite loop
            for event in pygame.event.get():
                if event.type == KEYDOWN:

                    if event.key == K_ESCAPE:  # for quiting the game using escape key
                        running = False
                    if event.key == K_RETURN:# for restart the game by pressing enter
                        pygame.mixer.music.unpause()
                        pause = False



                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()
                        if event.key == K_LEFT:
                            self.snake.move_left()  # we make a class for the movement of the block
                        if event.key == K_RIGHT:
                            self.snake.move_right()
                    elif event.type == QUIT:
                     running = False

            try:
                if not pause:# if game is paused i don't want to play game
                    self.play()# for the walk of the snake and apple draw
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()# for restarting the game

            time.sleep(0.1)  # as we introduce the loop the snake will move to fast so we have the time module for delay

if __name__ == "__main__":
    game = Game()
    game.run()
