import pygame
from pygame.locals import *
import csv
import os
fpsclock = pygame.time.Clock()
FPS = 30

pygame.init()

WINDOWWIDTH = 620
WINDOWHEIGHT = 620
LEFT_ADD = 100
DOWN_ADD = 100
tile_size = 15
tile_type = 15
rows = 66
cols = 61
num_map = 0
num_map_open = 1    
num_map_load = 1
num_map_new = 2
scroll_x = 0
scroll_y = 0
tile_count = 0
mouse_left, mouse_right = False,False
            
dir = "moew/"
dir2 = "map/"
dir3 = "img/button/"




save_img = pygame.transform.scale(pygame.image.load("tick.png"),(tile_size*2, tile_size*2))
load_img = pygame.transform.scale(pygame.image.load("reload.png"),(tile_size*2, tile_size*2))
x_img = pygame.transform.scale(pygame.image.load("not.png"),(tile_size*2, tile_size*2))
img1 = pygame.transform.scale(pygame.image.load("black.png"),(WINDOWWIDTH , WINDOWHEIGHT ))
screen = pygame.display.set_mode((WINDOWWIDTH + LEFT_ADD, WINDOWHEIGHT + DOWN_ADD))
pygame.display.set_caption("hehe")

class Button():
    def __init__(self,bt_img,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.bt_img = pygame.transform.scale(bt_img,(self.width,self.height))
        self.bt_rect = self.bt_img.get_rect(topleft = (self.x,self.y))
        self.clicked = False
    
    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()

        if self.bt_rect.collidepoint(pos):
            if mouse_left and not self.clicked:
                action = True
                self.clicked = True

        if not mouse_left:
            self.clicked = False

        surface.blit(self.bt_img,(self.x,self.y))
        return action
img_list = []
for i in range(tile_type):
    img = pygame.image.load(f'{dir}{i}.png')
    img = pygame.transform.scale(img,(tile_size,tile_size))
    img_list.append(img)

def draw_grid():
    for i in range(cols +1):
        pygame.draw.line(screen,( 250,250,250), (i* tile_size - scroll_x,0), (i * tile_size - scroll_x, WINDOWHEIGHT))
    for i in range(rows + 1):
        pygame.draw.line(screen,(250,250,250), (0, i * tile_size - scroll_y), (WINDOWWIDTH, i * tile_size - scroll_y))

def draw_bg():
    pygame.draw.rect(screen,(0,50,0),(WINDOWWIDTH,0 ,LEFT_ADD,WINDOWHEIGHT + DOWN_ADD))
    pygame.draw.rect(screen,(0,50,0),(0,WINDOWHEIGHT,WINDOWWIDTH + LEFT_ADD, DOWN_ADD))

# tạo một danh sách trống:
world_data = []
for row in range(rows):
    r = [-1] * cols
    world_data.append(r)

save_button = Button(save_img,WINDOWWIDTH - tile_size,WINDOWHEIGHT+50,tile_size*2,tile_size*2)
load_button = Button(load_img,WINDOWWIDTH +(tile_size*2),WINDOWHEIGHT+50,tile_size*2,tile_size*2)
x_button = Button(x_img,WINDOWWIDTH +(tile_size*5),WINDOWHEIGHT+50,tile_size*2,tile_size*2)


button_list = []
button_col = 0
button_row = 0
for i in range(len(img_list)):
	tile_button = Button(img_list[i],WINDOWWIDTH + (tile_size*2 * button_col) + tile_size, (tile_size*2 * button_row) + tile_size,tile_size,tile_size)
	button_list.append(tile_button)
	button_col += 1
	if button_col == 3:
		button_row += 1
		button_col = 0
    

    
def draw_text(text,x,y,Font,scale):
    font = pygame.font.Font(Font,scale)
    img = font.render(text, True, (250,250,250))
    screen.blit(img, (x, y))

def move():
    #dx = 0
    dy = 0
    global scroll_x, scroll_y
    global dx
    dx = 0 
    speed = 5
    if left:
        dx -= speed
    if right:
        dx += speed
    if up:
        dy -= speed
    if down:
        dy += speed
    scroll_x -= dx
    scroll_y -= dy
    
def draw_world():
    screen.blit(img1,(0,0))
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if tile > -1:
                screen.blit(img_list[tile], (x* tile_size - scroll_x, y * tile_size - scroll_y  ))
right ,left , up , down= False, False , False ,  False
mouse_left,mouse_right = False,False
run = True
load, save, create,max = True, False, False, False
while run:
    max_map = (len(os.listdir(f'{dir2}'))) - 1
    move()
    draw_world()
    draw_grid()
    draw_bg()
    draw_text(f"level: {num_map_load}",WINDOWWIDTH + 10,WINDOWHEIGHT /4 + 50,'VHARIABI.TTF',10)
    if max:
        draw_text(f"max level",WINDOWWIDTH +10 ,WINDOWHEIGHT /4 + 70,'VHARIABI.TTF',10)
    draw_text(f"Press ' W A S D ' to move",10,WINDOWHEIGHT + 10,'VHARIABI.TTF',10)
    draw_text(f"Press left/right to go to the next/previous level",10,WINDOWHEIGHT + 30,'VHARIABI.TTF',10)
    button_count = 0
    for button_count, i in enumerate(button_list):
        if i.draw(screen):
            tile_count = button_count
    if save_button.draw(screen) or save:
        create = False
        with open(f'{dir2}level_{num_map_open}_data.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter = ',')
            for row in world_data:
                writer.writerow(row)
    if load_button.draw(screen) or load :
       with open(f'{dir2}level_{num_map_load}_data.csv', newline='') as csvfile:
            hehe = csv.reader(csvfile, delimiter = ',')
            for x, row in enumerate(hehe):
                for y, tile in enumerate(row):
                    world_data[x][y] = int(tile)
    print(num_map_open,num_map_load,num_map_new,max_map)
    pygame.draw.rect(screen,(100,20,100),button_list[tile_count].bt_rect, 2)
    if x_button.draw(screen):
        run = False
    if create: 
        num_map_open = num_map_new
        num_map_load = 0
        draw_text(f"create new map",10,WINDOWHEIGHT + 50,'VHARIABI.TTF',10)
        draw_text(f"press enter to save",10,WINDOWHEIGHT + 70,'VHARIABI.TTF',10)
    else:
        num_map_load = num_map_open
        num_map_new = max_map +1
    pos = pygame.mouse.get_pos()
    x = (pos[0] + scroll_x) // tile_size
    y = (pos[1] + scroll_y) // tile_size
    if pos[0] < WINDOWWIDTH and pos[1] < WINDOWHEIGHT:
        if pygame.mouse.get_pressed()[0] == 1:
            if world_data[y][x] != tile_count:
                world_data[y][x] = tile_count
        if pygame.mouse.get_pressed()[2] == 1:
            world_data[y][x] = -1
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_left = True
            if event.button == 3:
                mouse_right = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mouse_left = False
            if event.button == 3:
                mouse_right = False
        if event.type == pygame.QUIT:
            run = False
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                create = False
                load = True
                num_map_open += 1
                if num_map_open >= max_map:
                    num_map_open = max_map
                    max = True
                else:
                    max = False
                num_map_load += 1
                if num_map_load >= max_map:
                    num_map_load = max_map
                    max = True
                else:
                    max = False 
                num_map_new += 1
            if event.key == K_LEFT:
                load = True
                num_map_open -= 1
                num_map_load -= 1
                if num_map_open <=1:
                    max = True
                    num_map_open = 1
                else:
                    max = False
                if num_map_load <=1:
                    max = True
                    num_map_load = 1
                else:
                    max = False
                num_map_new -= 1
            if event.key == K_UP:
                tile_size += 5
            if event.key == K_DOWN:
                tile_size -= 5
            if event.key == K_SPACE:
                #pass
                #run = False
                create = True
                load = True
            if event.key == K_a:
                right = True
            if event.key == K_d:
                left = True
            if event.key == K_w:
                down = True
            if event.key == K_s:
                up = True
            if event.key == K_RETURN:
                save = True
        if event.type == KEYUP:
            if event.key == K_a:
                right = False
            if event.key == K_d:
                left = False
            if event.key == K_w:
                down = False
            if event.key == K_s:
                up = False
            if event.key ==  K_LEFT:
                load = False
            if event.key ==  K_RIGHT:
                load = False
            if event.key == K_SPACE:
                load = False
            if event.key == K_RETURN:
                save = False
    pygame.display.update()
    fpsclock.tick(FPS)

pygame.quit()