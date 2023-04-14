
import pygame, math
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()
font = pygame.font.Font('arial.ttf', 25)
#font = pygame.font.SysFont('arial', 25)


##thigns we need to add
# reset function
# reward
# play(action) --> direction
# keep track fo game_iteration
# change if is collision fucntion


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4
    
Point = namedtuple('Point', 'x, y')

# rgb colors
WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)

BLOCK_SIZE = 20

GAME_SPEEDS = [10,20,40,200,1e99]

 

class SnakeGameAI:
    
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.reset()

        #interacitve game speed variables
        self.speed_index = 0
       

    def reset(self):
         # init game state
        self.direction = Direction.RIGHT
        
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, 
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        
        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0

        
    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE 
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()
        
    def play_step(self, action):
        self.frame_iteration += 1

        
        speed = GAME_SPEEDS[self.speed_index % 5]
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            #changes game speed interactively
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.speed_index += 1
                    speed = GAME_SPEEDS[self.speed_index % 5]
                    print(str(speed))



        
        
        # 2. move
        self._move(action) # update the head
        self.snake.insert(0, self.head)
        
        # 3. check if game over
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score
            
        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            reward = +10
            self._place_food()
        else:
            # if no food, remove the last pixel in list
            self.snake.pop()
            reward = -1
            
            
        
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(speed)
        # 6. return game over and score
        return reward, game_over, self.score
    
    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # hits boundary
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        # hits itself
        if pt in self.snake[1:]:
            return True
        
        return False
        
    def _update_ui(self):
        self.display.fill(BLACK)
        
        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))
            
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def distance_to_collision(self, look_direction=None):
        # [straight, right, left]
        # calculate distance to wall
        if look_direction is None:
            look_direction = self.direction

        wall_distance = 1e99
        if look_direction == Direction.RIGHT:
            wall_distance = self.w - self.head.x
        elif look_direction == Direction.UP:
            wall_distance = self.head.y
        elif look_direction == Direction.LEFT:
            wall_distance = self.head.x
        else:
            wall_distance = self.h - self.head.y

        tail_distance = 1e99
        # tail distance
        if look_direction == Direction.RIGHT:
            # 
            for snake_part in self.snake:
                if snake_part.y == self.head.y: # the y coord stays constant
                    if snake_part.x > self.head.x: # the tail part has to be right of the head
                        tail_distance = np.min( [tail_distance, np.abs(self.head.x - snake_part.x)] )
        elif look_direction == Direction.UP:
            for snake_part in self.snake:
                if snake_part.x == self.head.x: # the x coord stays constant
                    if snake_part.y < self.head.y: # the tail part has to be above  the head
                        tail_distance = np.min( [tail_distance, np.abs(self.head.y - snake_part.y)] )
    
        elif look_direction == Direction.LEFT:
            for snake_part in self.snake:                 
                 if snake_part.y == self.head.y: # the y coord stays constant
                    if snake_part.x < self.head.x: # the tail part has to be above  the head
                        tail_distance = np.min( [tail_distance, np.abs(self.head.x - snake_part.x)] )

        else:
            for snake_part in self.snake:
                 if snake_part.x == self.head.x: # the x coord stays constant
                    if snake_part.y > self.head.y: # the tail part has to be below the head
                        tail_distance = np.min( [tail_distance, np.abs(self.head.y - snake_part.y)] )
        
        #is true if snake is going towards its tail
        head_towards_tail = False
        if tail_distance < wall_distance:
            head_towards_tail = True



        return((np.min([tail_distance,wall_distance])),head_towards_tail)

    def find_tail_distance(self):
        #UNUSED
        head_x = self.head.x
        head_y = self.head.y
        tail_x = self.snake[-1].x
        tail_y = self.snake[-1].y

        tail_distance = math.sqrt((abs(head_x-tail_x))**2+(abs(head_y-tail_y))**2)

        return tail_distance

    def _move(self, action):
        # update the position of the head based on a command
        # [straight, right, left]

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)
     
        if np.array_equal(action, [1,0,0]): # go straight
            new_dir = clock_wise[idx] # no change
        elif np.array_equal(action, [0,1,0]): # go right
            next_idx = (idx+1) % 4
            new_dir = clock_wise[next_idx] # right turn r -> d -> l ->u
        else: #[0,0,1]                          # go left
            next_idx = (idx-1) % 4
            new_dir = clock_wise[next_idx] # right turn r -> u -> l -> u
        
        # this is the current direction that the worm is headed towards
        self.direction = new_dir
        
        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE
            
        self.head = Point(x, y)
