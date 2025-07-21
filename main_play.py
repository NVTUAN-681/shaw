import pygame
from pygame.locals import *
import os
import csv 
pygame.init()
fpsclock = pygame.time.Clock()
FPS = 30

# variable(biến)
WINDOWWIDTH = 700
WINDOWHEIGHT = 700
hero_width = 35
hero_height = 35
tile_size = 50
tile_type = 14 
level = 1
win = False 
ROWS = 66
COLS = 61

# dir
dir_map = "map_data/"
dir_bg = "img/bg/"
dir_button = 'img/button/'
dir_img_animation = 'img/img_animation/'
dir_items = 'img/items/'
dir_UI = 'img/User Interface/'
dir_wall = 'img/wall/'
dir_text = "text/"
dir_data = "map_data/map/"

# img (ảnh)
#bg:
img_bg1 = pygame.image.load(dir_bg + "bg1.jpg")
img_bg2 = pygame.image.load(dir_bg + "black.png")

#UI:
img_UI1 = pygame.image.load(dir_UI + "layla.jpg")
img_UI2 = pygame.image.load(dir_UI + "shield.png")
img_UI3 = pygame.image.load(dir_UI + "skull.png")
img_UI4 = pygame.image.load(dir_UI + "water.png")
img_UI5 = pygame.image.load(dir_UI + "ice.png")
img_UI6= pygame.image.load(dir_UI + "fire.png")
img_UI7 = pygame.image.load(dir_UI + "bush.png")
img_UI8 = pygame.image.load(dir_UI + "win.png")
img_UI9 = pygame.image.load(dir_UI + "lose.png")
img_UI10 = pygame.image.load(dir_UI + "Picture1.png") 

# map
img_wall1 = pygame.image.load(dir_wall + "wall.jpg")
img_wall2 = pygame.image.load(dir_wall + "wall_ice.jpg")
img_wall3 = pygame.image.load(dir_wall + "wall_fire.jpg")

#items
img_item1 = pygame.image.load(dir_items + "defence_fire.png")
img_item2 = pygame.image.load(dir_items + "defence_water.png")
img_item3 = pygame.image.load(dir_items + "defence_cold.png")
img_item4  = pygame.image.load(dir_items + "hp.png")
img_item5 = pygame.image.load(dir_items + "poison.png")
img_item6 = pygame.image.load(dir_items + "wind.png")

# button
img_bt1 = pygame.image.load(dir_button + "menu_table.png")
img_bt2 = pygame.image.load(dir_button + "play2.png")
img_bt3 = pygame.image.load(dir_button + "menu.png")
img_bt4 = pygame.image.load(dir_button + "table_pause.png")
img_bt5 = pygame.image.load(dir_button + "not.png")
img_bt6 = pygame.image.load(dir_button + "test.png") 
img_bt8 = pygame.image.load(dir_button + "menu_table2.png")
img_bt9 = pygame.image.load(dir_button + "nut1.png")
img_bt10 = pygame.image.load(dir_button + "table.png")
img_bt11 = pygame.image.load(dir_button + "reload.png")
img_bt12 = pygame.image.load(dir_button + "menu_table3.png")
img_bt13 = pygame.image.load(dir_button + "detail.png")
img_bt14 = pygame.image.load(dir_button + "tick.png")
img_bt15 = pygame.image.load(dir_button + "button.png")
# screen (màn hình)
icon = pygame.display.set_icon(img_UI1)
caption = pygame.display.set_caption("Labyrinth")
screen = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))

class Player():
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.animation_list = []
        self.animation_wind_list = []
        self.frame_index = 0
        self.frame_wind_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        self.update_time_wind = pygame.time.get_ticks()
        animation_types = ["chill","run","fly"]
        for animation in animation_types:
            temp_list = []
            num_frames = len(os.listdir(f'{dir_img_animation}hero/{animation}'))
            for i in range(num_frames):
                hero = pygame.image.load(f'{dir_img_animation}hero/{animation}/{i}.png')
                hero = pygame.transform.scale(hero,(self.width,self.height))
                temp_list.append(hero)
            self.animation_list.append(temp_list)
        self.hero = self.animation_list[self.action][self.frame_index]
        self.shield = pygame.transform.scale(img_UI2,(self.width + 20,self.height + 20))
        for i in range(6):
            wind = pygame.image.load(f'{dir_img_animation}wind/{i}.png')
            wind = pygame.transform.scale(wind,(self.width+ 50,self.height))
            self.animation_wind_list.append(wind)
        self.wind_img = self.animation_wind_list[self.frame_wind_index]
        self.wind_rect = self.wind_img.get_rect(topleft = (self.x,self.y))
        self.hero_rect = self.hero.get_rect(topleft = (self.x,self.y))
        self.hero_rect_ref = self.hero.get_rect(topleft = (self.x,self.y))
        self.speed = 8
        self.jump = -12
        self.vel_y = 0
        self.jump_cout = 0
        self.jump_check = True
        self.flip = False
        self.gap_x = int((WINDOWWIDTH - hero_width)/2)
        self.gap_y = int((WINDOWHEIGHT - hero_height)/2)
        self.dx = 0
        self.dy = 0
        self.scroll_x = 0
        self.scroll_y = 0
        self.alive = True
        self.hp = 100
        self.hp_max = 100
        self.tick_water = 0
        self.tick_fire = 0
        self.tick_cold = 0
        self.tick_poison = 0
        self.tick_wind = 0
        self.tick_tile = pygame.time.get_ticks()
        self.time_defence_water = pygame.time.get_ticks()
        self.time_defence_fire = pygame.time.get_ticks()
        self.time_defence_cold = pygame.time.get_ticks()
        self.time_poison = pygame.time.get_ticks()
        self.time_poison2 = pygame.time.get_ticks()
        self.time_wind = pygame.time.get_ticks()
        self.time = 0
        self.check_fire = False
        self.check_water = False
        self.check_cold = False
        self.check_health = False
        self.check_poison = False
        self.check_bush = False
        self.check_tile = False


    def move(self,up,down,left,right,World):
        FIRE_COOLDOWN = 2000
        WATER_COOLDOWN = 2000
        BUSH_COOLDOWN = 3000
        POISON_COOLDOWN = 500
        POISON_COOLDOWN2 = 4000
        DEFENCE_TIME = 1000

        inwater = False
        intile = False
        infire = False
        incold = False
        inbush = False
        inpoison = False

        fire_dame = 1
        water_dame = 1
        bush_dame = 1
        poison_dame = 1



        speed_ice = 2
        speed_swim = 4
        speed_air = 15
        speed = 8
        vel_y_swim = 1

        dx = 0
        dy = 0
        if dx >= speed:
            dx = speed
        if dx <= -speed:
            dx = - speed 
        dx_x = 0
        dy_y = 0
        if right:
            dx += self.speed
            dx_x = dx
            self.flip = False
        if left:
            dx -= self.speed
            dx_x = dx
            self.flip = True

        if True:
            self.vel_y +=1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y
            dy_y = dy
        

# di chuyển map:
        if World.tile_list[0][1].left < 0 and World.tile_list[-1][1].right > WINDOWWIDTH :
            if self.hero_rect.left + dx < self.gap_x  or self.hero_rect.right + dx > WINDOWWIDTH - self.gap_x :
                dx_x = 0
                self.scroll_x = -dx

        if World.tile_list[0][1].top < 0 and World.tile_list[-1][1].bottom > WINDOWHEIGHT:
            if self.hero_rect.bottom + dy > WINDOWHEIGHT - self.gap_y:
                dy_y = 0
                self.scroll_y = -dy
            if self.hero_rect.top + dy < self.gap_y:
                dy_y = 0
                self .scroll_y = -dy
# giữ map:
        # xét theo trục x        
        if World.tile_list[0][1].left >= 0 or World.tile_list[-1][1].right <= WINDOWWIDTH: 
            self.scroll_x = 0
            if World.tile_list[0][1].left >= 0 :
                if self.hero_rect.right + dx > WINDOWWIDTH - self.gap_x :
                    dx_x = 0
                    self.scroll_x = -dx
            if World.tile_list[-1][1].right <= WINDOWWIDTH: 
                if self.hero_rect.left + dx < self.gap_x :
                    dx_x = 0
                    self.scroll_x = -dx

        # xét theo trục y:   
        if World.tile_list[0][1].top  >= 0 or World.tile_list[-1][1].bottom <= WINDOWHEIGHT:
            self.scroll_y = 0  
            if World.tile_list[0][1].top >= 0:
                if self.hero_rect.bottom + dy > WINDOWHEIGHT - self.gap_y:           
                    dy_y  = 0
                    self.scroll_y = -dy
            if World.tile_list[-1][1].bottom  <= WINDOWHEIGHT:
                if self.hero_rect.top + dy < self.gap_y:
                    dy_y = 0
                    self.scroll_y = -dy


# kiểm tra va chạm
        # tường gạch thông thường 
        for World.tile in World.tile_list:
            if World.tile[2] == "wall":
                if World.tile[1].colliderect(self.hero_rect.x, self.hero_rect.y + dy,self.width,self.height): 
                    intile = True
                    if self.vel_y < 0: 
                        dy_y = 0
                        self.vel_y = 0  
                        self.scroll_y = 0
                    elif self.vel_y > 0:
                        self.jump_cout  = 0
                        self.jump_check = True
                        dy_y = 0
                        self.vel_y = 0     
                        self.scroll_y = 0
                        # trả lại tốc độ
                        if right:
                            if World.tile[1].colliderect(self.hero_rect.x - 30, self.hero_rect.y + dy, self.width,self.height):
                                self.speed = speed
                        if left:
                            if World.tile[1].colliderect(self.hero_rect.x + 30, self.hero_rect.y + dy, self.width,self.height):
                                self.speed = speed
                if World.tile[1].colliderect(self.hero_rect.x + dx, self.hero_rect.y ,self.width,self.height):
                    dx_x = 0
                    self.scroll_x = 0
            self.check_tile = intile
        # gạch băng
            if World.tile[2] == "wall_ice":
                if World.tile[1].colliderect(self.hero_rect.x, self.hero_rect.y + dy,self.width,self.height): 
                    if self.tick_cold == 0:
                        self.speed = speed_ice
                    incold = True
                    if self.vel_y < 0: 
                        dy_y = 0
                        self.vel_y = 0  
                        self.scroll_y = 0
                    elif self.vel_y > 0:
                        self.jump_cout  = 0
                        self.jump_check = True
                        dy_y = 0
                        self.vel_y = 0     
                        self.scroll_y = 0
                if World.tile[1].colliderect(self.hero_rect.x + dx, self.hero_rect.y  ,self.width,self.height):
                    dx_x = 0
                    self.scroll_x = 0
            self.check_cold = incold
        # tường gạch vỡ 
        for i in range(len(world.tile_break_list)):
            for World.tile in World.tile_break_list:
                if World.tile[1].colliderect(self.hero_rect.x ,self.hero_rect.y +dy , self.width,self.height):
                    intile = True
                    if self.vel_y < 0: 
                        dy_y = 0
                        self.vel_y = 0  
                        self.scroll_y = 0
                    elif self.vel_y > 0:
                        self.jump_cout  = 0
                        self.jump_check = True
                        dy_y = 0
                        self.vel_y = 0     
                        self.scroll_y = 0
                    if pygame.time.get_ticks() - World.update_time_tile_break  > 2000:
                        World.update_time_tile_break  = pygame.time.get_ticks()
                        World.frame_tile_break_index -= 1
                        World.tile_break_list.remove(World.tile)
                if World.tile[1].colliderect(self.hero_rect.x + dx, self.hero_rect.y , self.width,self.height):
                    dx_x = 0
                    self.scroll_x = 0
                    if pygame.time.get_ticks() - World.update_time_tile_break  > 2000:
                        World.update_time_tile_break  = pygame.time.get_ticks()
                        World.frame_tile_break_index -= 1
                        World.tile_break_list.remove(World.tile)
                self.check_tile = intile
        # nước
        for World.tile in World.water1_list:
            if World.tile[1].colliderect(self.hero_rect):
                inwater = True
                self.speed = speed_swim
                if self.check_cold == True and self.tick_cold == 0:
                    self.speed = speed_ice
                self.vel_y += 0.1
                if self.vel_y >= vel_y_swim:
                    self.vel_y = vel_y_swim
                if self.jump_check:
                    if up:
                        self.vel_y = -6
                for World.tile in World.tile_list:
                    if World.tile[1].colliderect(self.hero_rect.x, self.hero_rect.y + dy,self.width,self.height): 
                        if self.vel_y < 0: 
                            dy_y = 0
                            self.vel_y = 0  
                            self.scroll_y = 0
                        elif self.vel_y > 0:
                            self.jump_cout  = 0
                            self.jump_check = True
                            dy_y = 0
                            self.vel_y = 0     
                            self.scroll_y = 0
                    if World.tile[1].colliderect(self.hero_rect.x + dx, self.hero_rect.y ,self.width,self.height):
                        dx_x = 0
                        self.scroll_x = 0
                if pygame.time.get_ticks() - self.time_defence_water > DEFENCE_TIME:
                    self.time_defence_water = pygame.time.get_ticks()
                    self.tick_water -= 1
                    if self.tick_water <= 0:
                        self.tick_water = 0
                    if self.tick_water == 0:
                        if pygame.time.get_ticks() - self.time > WATER_COOLDOWN:
                            self.time = pygame.time.get_ticks()
                            self.hp -= water_dame    
        for World.tile in World.water2_list:
            jump_cout_water = 0
            if World.tile[1].colliderect(self.hero_rect):
                self.jump_cout = 0
                self.jump_check = True
                inwater = True
                self.speed = speed_swim
                if self.check_cold == True and self.tick_cold == 0:
                    self.speed = speed_ice
                self.vel_y += 0.1
                if self.vel_y >= vel_y_swim:
                    self.vel_y = vel_y_swim
                if self.jump_check:
                    if up:
                        self.vel_y = -6
                for World.tile in World.tile_list:
                    if World.tile[1].colliderect(self.hero_rect.x, self.hero_rect.y + dy,self.width,self.height): 
                        if self.vel_y < 0: 
                            dy_y = 0
                            self.vel_y = 0  
                            self.scroll_y = 0
                        elif self.vel_y > 0:
                            self.jump_cout  = 0
                            self.jump_check = True
                            dy_y = 0
                            self.vel_y = 0     
                            self.scroll_y = 0
                    if World.tile[1].colliderect(self.hero_rect.x + dx, self.hero_rect.y ,self.width,self.height):
                        dx_x = 0
                        self.scroll_x = 0
                if pygame.time.get_ticks() - self.time_defence_water > DEFENCE_TIME:
                    self.time_defence_water = pygame.time.get_ticks()
                    self.tick_water -= 1
                    if self.tick_water <= 0:
                        self.tick_water = 0
                    if self.tick_water == 0:
                        if pygame.time.get_ticks() - self.time > WATER_COOLDOWN:
                            self.time = pygame.time.get_ticks()
                            if self.tick_poison !=0:
                                self.hp -= (water_dame *2)
                            else:
                                self.hp -= water_dame
            self.check_water = inwater 

        #lửa
        for World.fire_tile in World.fire_list:
            if World.fire_tile[1].colliderect(self.hero_rect):
                infire = True
                if pygame.time.get_ticks() - self.time_defence_fire > DEFENCE_TIME :
                    self.time_defence_fire = pygame.time.get_ticks()
                    self.tick_fire -=1
                    if self.tick_fire <=0:
                        self.tick_fire = 0
                    if self.tick_fire == 0:
                        if pygame.time.get_ticks() - self.time > FIRE_COOLDOWN:
                            self.time = pygame.time.get_ticks()
                            if self.tick_poison !=0:
                                self.hp -= (fire_dame *2)
                            else:
                                self.hp -= fire_dame
        self.check_fire = infire 

        # bui:
        for World.tile in World.bush_list:
            if World.tile[1].colliderect(self.hero_rect):
                inbush = True
                self.jump_check = False
                if pygame.time.get_ticks() - self.time > BUSH_COOLDOWN:
                    self.time = pygame.time.get_ticks()
                    if self.tick_poison !=0:
                        self.hp -= (bush_dame *2)
                    else:
                        self.hp -= bush_dame
        self.check_bush = inbush

        # độc
        for World.tile in World.poison_list:
            if World.tile[1].colliderect(self.hero_rect):
                self.tick_poison = 10
                inpoison = True
                if pygame.time.get_ticks() - self.time_poison > POISON_COOLDOWN2:
                    self.time_poison = pygame.time.get_ticks()
                    self.hp -= poison_dame
        self.check_poison = inpoison

        # vật phẩm hỗ trợ
        for World.tile in World.items_list:
            if World.tile[2] == 'health':
                if self.hp < 100:
                    if World.tile[1].colliderect(self.hero_rect):
                        World.items_list.remove(World.tile)
                        self.hp += 20
                        self.tick_poison = 0
                        break
            if World.tile[2] == 'defence_fire':
                if World.tile[1].colliderect(self.hero_rect):
                    World.items_list.remove(World.tile)
                    self.tick_fire += 10
                    break
            if World.tile[2] == 'defence_water':
                if World.tile[1].colliderect(self.hero_rect):
                    World.items_list.remove(World.tile)
                    self.tick_water += 10
                    break
            if World.tile[2] == 'defence_cold':
                if World.tile[1].colliderect(self.hero_rect):
                    World.items_list.remove(World.tile)
                    self.tick_cold += 10
                    break
            if World.tile[2] == "cure":
                if World.tile[1].colliderect(self.hero_rect):
                    World.items_list.remove(World.tile)
                    self.tick_poison = 0
            if World.tile[2] == "wind":
                if World.tile[1].colliderect(self.hero_rect):
                    World.items_list.remove(World.tile)
                    self.tick_wind += 10


        # you win:
        for World.tile in World.win_list:
            if World.tile[1].colliderect(self.hero_rect):
                global win
                win = True


        # thời gian kháng hiệu ứng
        if pygame.time.get_ticks() - self.time_defence_fire > DEFENCE_TIME:
            self.time_defence_fire = pygame.time.get_ticks()
            self.tick_fire -= 1
            if self.tick_fire <= 0:
               self.tick_fire = 0 
        if not self.check_water:
            if self.tick_water <= 10:
                self.tick_water = 10
        if self.tick_water > 10:
            if pygame.time.get_ticks() - self.time_defence_water > DEFENCE_TIME:
                self.time_defence_water = pygame.time.get_ticks()
                self.tick_water -= 1
        if pygame.time.get_ticks() - self.time_defence_cold > DEFENCE_TIME:
            self.time_defence_cold = pygame.time.get_ticks()
            self.tick_cold -= 1
            if self.tick_cold <= 0:
               self.tick_cold = 0 

        # kiểm tra tương tắc thuộc tính + tương tác hoạt họa(animation)
        if not self.check_poison:
            if self.tick_poison != 0:
                if pygame.time.get_ticks() - self.time_poison2 > POISON_COOLDOWN:
                    self.time_poison2 = pygame.time.get_ticks()
                    self.tick_poison -= 1
                    
                    if self.tick_poison <= 0:
                        self.tick_poison = 0
        if self.tick_wind != 0:
            self.speed = speed_air
            if pygame.time.get_ticks() - self.time_wind > DEFENCE_TIME * 2:
                self.time_wind = pygame.time.get_ticks()
                self.tick_wind -=1
                if self.tick_wind <= 0:
                    self.tick_wind = 0

        # speed:
        if self.tick_wind != 0:
            self.speed = speed_air
            if pygame.time.get_ticks() - self.time_wind > DEFENCE_TIME:
                self.time_wind = pygame.time.get_ticks()
                self.tick_wind -=1
                if self.tick_wind <= 0:
                    self.tick_wind = 0
            elif self.check_water and self.tick_wind != 0:
                    self.speed = speed
            elif self.check_water:
                self.speed = speed_swim
            elif self.check_cold:
                self.speed = speed_ice

        # action:
        if self.check_tile and (right or left):
            self.action = 1
        elif not self.check_tile and not self.check_water:
            self.action = 2
        else:
            self.action = 0
        if self.check_water or self.check_cold:
            self.action = 0
            

            
        # kiểm tra sư sống
        if self.hp >= player1.hp_max:
            self.hp = player1.hp_max
        if self.hp <= 0:
            self.hp = 0
            self.alive = False
            print("die")
        else:
            self.alive = True
            

        self.hero_rect.top += dy_y
        self.hero_rect.left += dx_x
        self.hero_rect_ref.top =  self.hero_rect.top + bg2.y
        self.hero_rect_ref.left = self.hero_rect.left + bg2.x
        self.wind_rect.top += dy_y
        self.wind_rect.left += dx_x
        self.dx = dx
        self.dy = dy

    def update_animation(self):
        ANIMATION_COOLDOWN = 100
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0
        self.hero = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time_wind > ANIMATION_COOLDOWN:
            self.update_time_wind = pygame.time.get_ticks()
            self.frame_wind_index += 1
        if self.frame_wind_index >= len(self.animation_wind_list):
            self.frame_wind_index = 0
        self.wind_img = self.animation_wind_list[self.frame_wind_index]
    def undate_aciton(self,new_aciton):
        if new_aciton != self.action:
            self.action = new_aciton
            self.frame_index +=1
            self.update_time = pygame.time.get_ticks()

    def draw(self):
        if self.tick_wind != 0:
            screen.blit(pygame.transform.flip(self.wind_img, self.flip, False),(self.wind_rect.left - 20,self.wind_rect.top))
        screen.blit(pygame.transform.flip(self.hero, self.flip, False),(self.hero_rect_ref.left , self.hero_rect_ref.top))
        #pygame.draw.rect(screen,(150,250,250),self.hero_rect,(1))

    
class BG():
    def __init__(self,bg_img,x,y,width,height,scale):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.scale = scale
        self.bg = pygame.transform.scale(bg_img,(self.width * self.scale,self.height * self.scale))
        self.bg_rect = self.bg.get_rect(topleft = (self.x,self.y))
        self.scroll_x = 0
        self.scroll_y = 0
        self.update_time = pygame.time.get_ticks()


    def move(self, player1,World):
        for World.tile in World.tile_list: 
            if player1.hero_rect.left + player1.dx < player1.gap_x or player1.hero_rect.right + player1.dx > WINDOWWIDTH - player1.gap_x:
                World.tile[1].x += player1.scroll_x
            if player1.hero_rect.top + player1.dy < player1.gap_y or player1.hero_rect.bottom + player1.dy > WINDOWWIDTH - player1.gap_y:
                World.tile[1].y += player1.scroll_y

        for World.tile in World.tile_break_list:
            if player1.hero_rect.left + player1.dx < player1.gap_x or player1.hero_rect.right + player1.dx > WINDOWWIDTH - player1.gap_x:
                World.tile[1].x += player1.scroll_x
            if player1.hero_rect.top + player1.dy < player1.gap_y or player1.hero_rect.bottom + player1.dy > WINDOWWIDTH - player1.gap_y:
                World.tile[1].y += player1.scroll_y

        for World.tile in World.fire_list:
            if player1.hero_rect.left + player1.dx < player1.gap_x or player1.hero_rect.right + player1.dx > WINDOWWIDTH - player1.gap_x:
                World.tile[1].x += player1.scroll_x
            if player1.hero_rect.top + player1.dy < player1.gap_y or player1.hero_rect.bottom + player1.dy > WINDOWWIDTH - player1.gap_y:
                World.tile[1].y += player1.scroll_y

        for World.tile in World.water1_list:
            if player1.hero_rect.left + player1.dx < player1.gap_x or player1.hero_rect.right + player1.dx > WINDOWWIDTH - player1.gap_x:
                World.tile[1].x += player1.scroll_x
            if player1.hero_rect.top + player1.dy < player1.gap_y or player1.hero_rect.bottom + player1.dy > WINDOWWIDTH - player1.gap_y:
                World.tile[1].y += player1.scroll_y       

        for World.tile in World.water2_list:
            if player1.hero_rect.left + player1.dx < player1.gap_x or player1.hero_rect.right + player1.dx > WINDOWWIDTH - player1.gap_x:
                World.tile[1].x += player1.scroll_x
            if player1.hero_rect.top + player1.dy < player1.gap_y or player1.hero_rect.bottom + player1.dy > WINDOWWIDTH - player1.gap_y:
                World.tile[1].y += player1.scroll_y    

        for World.tile in World.bush_list:
            if player1.hero_rect.left + player1.dx < player1.gap_x or player1.hero_rect.right + player1.dx > WINDOWWIDTH - player1.gap_x:
                World.tile[1].x += player1.scroll_x
            if player1.hero_rect.top + player1.dy < player1.gap_y or player1.hero_rect.bottom + player1.dy > WINDOWWIDTH - player1.gap_y:
                World.tile[1].y += player1.scroll_y   
            
        for World.tile in World.poison_list:
            if player1.hero_rect.left + player1.dx < player1.gap_x or player1.hero_rect.right + player1.dx > WINDOWWIDTH - player1.gap_x:
                World.tile[1].x += player1.scroll_x
            if player1.hero_rect.top + player1.dy < player1.gap_y or player1.hero_rect.bottom + player1.dy > WINDOWWIDTH - player1.gap_y:
                World.tile[1].y += player1.scroll_y   

        for World.tile in World.items_list:
            if player1.hero_rect.left + player1.dx < player1.gap_x or player1.hero_rect.right + player1.dx > WINDOWWIDTH - player1.gap_x:
                World.tile[1].x += player1.scroll_x
            if player1.hero_rect.top + player1.dy < player1.gap_y or player1.hero_rect.bottom + player1.dy > WINDOWWIDTH - player1.gap_y:
                World.tile[1].y += player1.scroll_y

        for World.tile in World.win_list:
            if player1.hero_rect.left + player1.dx < player1.gap_x or player1.hero_rect.right + player1.dx > WINDOWWIDTH - player1.gap_x:
                World.tile[1].x += player1.scroll_x
            if player1.hero_rect.top + player1.dy < player1.gap_y or player1.hero_rect.bottom + player1.dy > WINDOWWIDTH - player1.gap_y:
                World.tile[1].y += player1.scroll_y



            '''     
            if self.x < -(WINDOWWIDTH * self.scale) + WINDOWWIDTH:
                self.x = -(WINDOWWIDTH * self.scale) + WINDOWWIDTH
            if self.x > 0 :
                self.x = 0
            if self.y < -(WINDOWHEIGHT * self.scale) + WINDOWHEIGHT:
                self.y = -(WINDOWHEIGHT * self.scale)+ WINDOWHEIGHT
            if self.y > 0:
                self.y = 0
            '''
    def draw(self):
        screen.blit(self.bg,(self.x,self.y))

    def draw_menu(self):
        screen.blit(pygame.transform.scale(img_UI10,(150,110)),(0,0))
        if player1.tick_cold !=0 or player1.tick_fire != 0 or player1.tick_water > 10:
            screen.blit(player1.shield,(player1.hero_rect.left - 10,player1.hero_rect.top - 10))
        pygame.draw.rect(screen, (0,0,0),(20,30,100,12))
        pygame.draw.rect(screen,(100,100,100),(20,20,30,10))
        pygame.draw.rect(screen, (250,250,250),(20,30, int(1*player1.hp) , 12))
        pygame.draw.rect(screen,(50,50,50),(20,30,100,15),(3))

        if player1.tick_wind > 0:
            screen.blit(pygame.transform.scale(img_item6,(25,25)),(100,50))
        if player1.tick_fire > 0:
            screen.blit(pygame.transform.scale(img_item1,(25,25)),(25,50))
        if player1.tick_cold > 0:
            screen.blit(pygame.transform.scale(img_item3,(25,25)),(50,50))
        if player1.tick_water > 10:
            screen.blit(pygame.transform.scale(img_item2,(25,25)),(75,50))
        if player1.check_water:
            if player1.tick_water != 0:
                screen.blit(pygame.transform.scale(img_item2,(25,25)),(50,50))
                screen.blit(player1.shield,(player1.hero_rect.left - 10,player1.hero_rect.top - 10))
        if player1.check_water:
            screen.blit(pygame.transform.scale(img_UI4,(20,20)),(15,80))
        if player1.check_fire and player1.tick_fire == 0:
            screen.blit(pygame.transform.scale(img_UI6,(20,20)),(35,80))
        if player1.check_cold and player1.tick_cold == 0:
            screen.blit(pygame.transform.scale(img_UI5,(20,20)),(55,80))
        if player1.tick_poison != 0:
            screen.blit(pygame.transform.scale(img_UI3,(20,20)),(75,80))
        if player1.check_bush:
            screen.blit(pygame.transform.scale(img_UI7,(20,20)),(95,80))

class Button():
    def __init__(self,bt_img,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.bt_img = pygame.transform.scale(bt_img,(self.width,self.height))
        self.bt_rect = self.bt_img.get_rect(center = (self.x,self.y))
        self.clicked = False
    
    def check(self):
        action = False
        pos = pygame.mouse.get_pos()

        if self.bt_rect.collidepoint(pos):
            if mouse_left and not self.clicked:
                action = True
                self.clicked = True

        if not mouse_left:
            self.clicked = False
        return action
    def draw(self):
        screen.blit(self.bt_img,(self.x - self.width/2,self.y - self.height/2))

class Text():
    def __init__(self, text,x,y,font,scale):
        self.text = text
        self.x = x
        self.y = y
        self.scale = scale
        self.font =  pygame.font.Font(font,self.scale)
        self.text_surface = self.font.render(self.text,True,(255,255,255))
        self.text_rect = self.text_surface.get_rect(center = (self.x,self.y))
        self.text_width = self.text_surface.get_width()
        self.text_height = self.text_surface.get_height()
        self.clicked = False
    
    def update(self,update_new):
        self.new_text = str(update_new)
        self.text_surface = self.font.render(self.text,True,(255,255,255))
        self.text_rect = self.text_surface.get_rect(center = (self.x,self.y))
        self.text_width = self.text_surface.get_width()
        self.text_height = self.text_surface.get_height()

    def check(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.text_rect.collidepoint(pos):
            if mouse_left and not self.clicked:
                action = True
                self.clicked = True
            
            if not mouse_left:
                self.clicked = False
        return action
    def draw(self):
        screen.blit(self.text_surface,(self.x - self.text_width/2, self.y - self.text_height/2))
        
class World():
    def __init__(self,data):
        self.num_cols = len(data[0])
        self.check = False
        self.tile_list = []
        self.tile_break_list = []
        self.ice_tile_list = []
        self.fire_tile_list = []
        self.bush_list = []
        self.poison_list = []
        self.water1_list = []
        self.water2_list = []
        self.fire_list = []
        self.items_list = []
        self.win_list = []

        self.animation_tile_break_list = []
        self.animation_fire_list = []
        self.animation_water1_list = []
        self.animation_water2_list = []
        self.animation_bush_list = []
        self.animation_poison_list = []
        self.animation_win_list = []

        self.frame_tile_break_index = 0
        self.frame_bush_index = 0
        self.frame_fire_index = 0
        self.frame_water1_index = 0
        self.frame_water2_index = 0
        self.frame_water_index = 0
        self.frame_poison_index = 0
        self.frame_win_index = 0

        self.update_time_tile_break = pygame.time.get_ticks()
        self.update_time_fire = pygame.time.get_ticks()
        self.update_time_water1 = pygame.time.get_ticks()
        self.update_time_water2 = pygame.time.get_ticks()
        self.update_time_bush= pygame.time.get_ticks()
        self.update_time_poison= pygame.time.get_ticks()
        self.update_time_win = pygame.time.get_ticks()
        self.scroll_x = 0
        self.scroll_y = 0
        row_cout = 0
        for row in world_data:
            col_cout = 0
            for tile in row:
                if tile == 0: # tường
                    self.type = "wall"
                    self.wall_img = pygame.transform.scale(img_wall1,(tile_size,tile_size))
                    self.img_rect = self.wall_img.get_rect()
                    self.img_rect.x = tile_size * col_cout
                    self.img_rect.y = tile_size * row_cout
                    self.wall_tile = (self.wall_img, self.img_rect,self.type)
                    self.tile_list.append(self.wall_tile)
                if tile == 1:
                    self.type = "wall_ice"
                    self.wall_ice_img = pygame.transform.scale(img_wall2,(tile_size,tile_size))
                    self.ice_rect = self.wall_ice_img.get_rect()
                    self.ice_rect.x = tile_size * col_cout
                    self.ice_rect.y = tile_size * row_cout
                    self.wall_ice_tile = (self.wall_ice_img, self.ice_rect,self.type)
                    self.tile_list.append(self.wall_ice_tile)
                if tile == 2:
                    self.type = "tile_break"
                    for i in range(5):
                        tile_break_img = pygame.image.load(f'{dir_img_animation}wall/{i}.png').convert_alpha()
                        tile_break_img = pygame.transform.scale(tile_break_img,(tile_size,tile_size)).convert_alpha()
                        self.animation_tile_break_list.append(tile_break_img)
                    self.tile_break_img = self.animation_tile_break_list[self.frame_tile_break_index]
                    self.tile_break_rect = self.tile_break_img.get_rect()
                    self.tile_break_rect.x = tile_size * col_cout
                    self.tile_break_rect.y = tile_size * row_cout
                    self.tile_break_tile = (self.tile_break_img, self.tile_break_rect,self.type)
                    self.tile_break_list.append(self.tile_break_tile)
                if tile == 3:
                    self.type = "fire"
                    for i in range(12):
                        fire_img = pygame.image.load(f'{dir_img_animation}fire/{i}.png').convert_alpha()
                        fire_img = pygame.transform.scale(fire_img,(tile_size,tile_size)).convert_alpha()
                        self.animation_fire_list.append(fire_img)
                    self.fire_img = self.animation_fire_list[self.frame_fire_index]
                    self.fire_rect = self.fire_img.get_rect()
                    self.fire_rect.x = tile_size * col_cout
                    self.fire_rect.y = tile_size * row_cout
                    self.fire_tile = (self.fire_img, self.fire_rect)
                    self.fire_list.append(self.fire_tile)
                if tile == 4:
                    self.type = "poison"
                    for i in range(12):
                        poison_img = pygame.image.load(f'{dir_img_animation}poison/{i}.png').convert_alpha()
                        poison_img = pygame.transform.scale(poison_img,(tile_size,tile_size)).convert_alpha()
                        self.animation_poison_list.append(poison_img)
                    self.poison_img = self.animation_poison_list[self.frame_poison_index]
                    self.poison_rect = self.poison_img.get_rect()
                    self.poison_rect.x = tile_size * col_cout
                    self.poison_rect.y = tile_size * row_cout
                    self.poison_tile = (self.poison_img, self.poison_rect,self.type)
                    self.poison_list.append(self.poison_tile)

                if tile == 5:
                    self.type = "bush"
                    for i in range(4):
                        bush_img = pygame.image.load(f'{dir_img_animation}bush/{i}.png').convert_alpha()
                        bush_img = pygame.transform.scale(bush_img,(tile_size,tile_size)).convert_alpha()
                        self.animation_bush_list.append(bush_img)
                    self.bush_img = self.animation_bush_list[self.frame_bush_index]
                    self.bush_rect = self.bush_img.get_rect()
                    self.bush_rect.x = tile_size * col_cout
                    self.bush_rect.y = tile_size * row_cout
                    self.bush_tile = (self.bush_img, self.bush_rect,self.type)
                    self.bush_list.append(self.bush_tile)

                if tile == 6:
                    self.type = "water1"
                    for i in range(3):
                        water1_img = pygame.image.load(f'{dir_img_animation}water1/{i}.png').convert_alpha()
                        water1_img = pygame.transform.scale(water1_img,(tile_size,tile_size)).convert_alpha()
                        self.animation_water1_list.append(water1_img)
                    self.water1_img = self.animation_water1_list[self.frame_water1_index]
                    self.water1_rect = self.water1_img.get_rect()
                    self.water1_rect.x = tile_size * col_cout
                    self.water1_rect.y = tile_size * row_cout
                    self.water1_tile = (self.water1_img, self.water1_rect,self.type)
                    self.water1_list.append(self.water1_tile)
                if tile == 7 :
                    self.type = "water2"
                    for i in range(2):
                        water2_img = pygame.image.load(f'{dir_img_animation}water2/{i}.png').convert_alpha()
                        water2_img = pygame.transform.scale(water2_img,(tile_size,tile_size)).convert_alpha()
                        self.animation_water2_list.append(water2_img)
                    self.water2_img = self.animation_water2_list[self.frame_water2_index]
                    self.water2_rect = self.water2_img.get_rect()
                    self.water2_rect.x = tile_size * col_cout
                    self.water2_rect.y = tile_size * row_cout
                    self.water2_tile = (self.water2_img, self.water2_rect,self.type)
                    self.water2_list.append(self.water2_tile)   
                
                if tile == 8:
                    self.type = "wind"
                    self.wind_img = pygame.transform.scale(img_item6,(tile_size,tile_size))
                    self.wind_rect = self.wind_img.get_rect()
                    self.wind_rect.centerx = tile_size * col_cout + tile_size/2
                    self.wind_rect.centery = tile_size * row_cout + tile_size/2
                    self.wind_tile = (self.wind_img,self.wind_rect,self.type)
                    self.items_list.append(self.wind_tile)
               
                if tile == 9:
                    self.type = "defence_fire"
                    self.defence_fire_img = pygame.transform.scale(img_item1,(tile_size,tile_size))
                    self.defence_fire_rect = self.defence_fire_img.get_rect()
                    self.defence_fire_rect.centerx = tile_size * col_cout + tile_size/2
                    self.defence_fire_rect.centery = tile_size * row_cout + tile_size/2
                    self.defence_fire_tile = (self.defence_fire_img,self.defence_fire_rect,self.type)
                    self.items_list.append(self.defence_fire_tile)
                if tile == 10:
                    self.type = "defence_water"
                    self.defence_water_img = pygame.transform.scale(img_item2,(tile_size,tile_size))
                    self.defence_water_rect = self.defence_water_img.get_rect()
                    self.defence_water_rect.centerx = tile_size * col_cout + tile_size/2
                    self.defence_water_rect.centery = tile_size * row_cout + tile_size/2
                    self.defence_water_tile = (self.defence_water_img,self.defence_water_rect,self.type)
                    self.items_list.append(self.defence_water_tile)
                if tile == 11:
                    self.type = "defence_cold"
                    self.defence_cold_img = pygame.transform.scale(img_item3,(tile_size,tile_size))
                    self.defence_cold_rect = self.defence_cold_img.get_rect()
                    self.defence_cold_rect.centerx = tile_size * col_cout + tile_size/2
                    self.defence_cold_rect.centery = tile_size * row_cout + tile_size/2
                    self.defence_cold_tile = (self.defence_cold_img,self.defence_cold_rect,self.type)
                    self.items_list.append(self.defence_cold_tile)
                if tile == 12:
                    self.type = "health"
                    self.health_img = pygame.transform.scale(img_item4,(tile_size/2,tile_size/2))
                    self.health_rect = self.health_img.get_rect()
                    self.health_rect.centerx = tile_size * col_cout + tile_size/2 
                    self.health_rect.centery = tile_size * row_cout + tile_size/2
                    self.health_tile = (self.health_img, self.health_rect,self.type)
                    self.items_list.append(self.health_tile)
                if tile == 13:
                    self.type = "cure"
                    self.cure_img = pygame.transform.scale(img_item5,(tile_size/2,tile_size/2))
                    self.cure_rect = self.cure_img.get_rect()
                    self.cure_rect.centerx = tile_size * col_cout + tile_size/2
                    self.cure_rect.centery = tile_size * row_cout + tile_size/2
                    self.cure_tile = (self.cure_img, self.cure_rect,self.type)
                    self.items_list.append(self.cure_tile)
                
                if tile == 14:
                    self.type = "win"
                    for i in range(12):
                        win_img = pygame.image.load(f'{dir_img_animation}win_point/{i}.png').convert_alpha()
                        win_img = pygame.transform.scale(win_img,(tile_size,tile_size)).convert_alpha()
                        self.animation_win_list.append(win_img)
                    self.win_img = self.animation_win_list[self.frame_win_index]
                    self.win_rect = self.win_img.get_rect()
                    self.win_rect.x = tile_size * col_cout
                    self.win_rect.y = tile_size * row_cout
                    self.win_tile = (self.win_img, self.win_rect,self.type)
                    self.win_list.append(self.win_tile)

                col_cout +=1
            row_cout += 1
            self.num_rows = row_cout


    def update_animation(self):
        ANIMATION_COOLDOWN = 80

        if pygame.time.get_ticks() - self.update_time_fire > ANIMATION_COOLDOWN:
            self.frame_fire_index += 1
            self.update_time_fire = pygame.time.get_ticks()
            if self.frame_fire_index >= len(self.animation_fire_list):
                self.frame_fire_index = 0
        self.fire_img = self.animation_fire_list[self.frame_fire_index]
        new_fire_list = []
        for i, (fire_img, fire_rect) in enumerate(self.fire_list):
            new_fire_list.append((self.fire_img,fire_rect))
        self.fire_list = new_fire_list

        if pygame.time.get_ticks() - self.update_time_water1 > ANIMATION_COOLDOWN:
            self.frame_water1_index += 1
            self.update_time_water1 = pygame.time.get_ticks()
            if self.frame_water1_index >= len(self.animation_water1_list):
                self.frame_water1_index = 0
        self.water1_img = self.animation_water1_list[self.frame_water1_index]
        new_water1_list = []
        for i, (_, water1_rect,type) in enumerate(self.water1_list):
            new_water1_list.append((self.water1_img,water1_rect,type))
        self.water1_list = new_water1_list

        if pygame.time.get_ticks() - self.update_time_water2 > ANIMATION_COOLDOWN:
            self.frame_water2_index += 1
            self.update_time_water2 = pygame.time.get_ticks()
            if self.frame_water2_index >= len(self.animation_water2_list):
                self.frame_water2_index = 0
        self.water2_img = self.animation_water2_list[self.frame_water2_index]
        new_water2_list = []
        for i, (water2_img, water2_rect,type) in enumerate(self.water2_list):
            new_water2_list.append((self.water2_img,water2_rect,type))
        self.water2_list = new_water2_list

        if pygame.time.get_ticks() - self.update_time_bush> ANIMATION_COOLDOWN:
            self.frame_bush_index += 1
            self.update_time_bush= pygame.time.get_ticks()
            if self.frame_bush_index >= len(self.animation_bush_list):
                self.frame_bush_index = 0
        self.bush_img = self.animation_bush_list[self.frame_bush_index]
        new_bush_list =[]
        for i,(bush_img,bush_rect,type) in enumerate(self.bush_list):
            new_bush_list.append((self.bush_img,bush_rect,type)) 
        self.bush_list = new_bush_list

        if pygame.time.get_ticks() - self.update_time_poison> ANIMATION_COOLDOWN:
            self.frame_poison_index += 1
            self.update_time_poison= pygame.time.get_ticks()
            if self.frame_poison_index >= len(self.animation_poison_list):
                self.frame_poison_index = 0
        self.poison_img = self.animation_poison_list[self.frame_poison_index]
        new_poison_list =[]
        for i,(poison_img,poison_rect,type) in enumerate(self.poison_list):
            new_poison_list.append((self.poison_img,poison_rect,type)) 
        self.poison_list = new_poison_list

        if pygame.time.get_ticks() - self.update_time_win > ANIMATION_COOLDOWN:
            self.frame_win_index += 1
            self.update_time_win = pygame.time.get_ticks()
            if self.frame_win_index >= len(self.animation_win_list):
                self.frame_win_index = 0
        self.win_img = self.animation_win_list[self.frame_win_index]
        new_win_list = []
        for i, (win_img,win_rect,type) in enumerate(self.win_list):
            new_win_list.append((self.win_img,win_rect,type))
        self.win_list = new_win_list

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0],tile[1])

        for tile in self.tile_break_list:
            screen.blit(tile[0],tile[1])

        for tile in self.ice_tile_list:
            screen.blit(tile[0],tile[1])
            
        for tile in self.water1_list:
            screen.blit(tile[0],tile[1])  

        for tile in self.water2_list:
            screen.blit(tile[0],tile[1]) 

        for tile in self.bush_list:
            screen.blit(tile[0],tile[1]) 
        
        for tile in self.poison_list:
            screen.blit(tile[0],tile[1]) 

        for fire_tile in self.fire_list:
            screen.blit(fire_tile[0],fire_tile[1])

        for tile in self.items_list:
            screen.blit(tile[0], tile[1])
        
        for tile in self.win_list:
            screen.blit(tile[0], tile[1])
        
            
world_data = []
for row in range(ROWS):
    r =[-1] * COLS
    world_data.append(r)

with open(f'{dir_data}level_{level}_data.csv', newline = '') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)
    

world = World(world_data)
menu = Button(img_bt3,WINDOWWIDTH - 50, 50,50,50)
# start
button_start1 = Button(img_bt9,WINDOWWIDTH/10 *1.5,WINDOWHEIGHT/10 * 7.9,200,80)
button_start2 = Button(img_bt9,WINDOWWIDTH/10 *8.5,WINDOWHEIGHT/10 * 7.9,200,80)

# pause
button_menu_pause = Button(img_bt4,WINDOWWIDTH/2,WINDOWHEIGHT/2,500,350)
button_play = Button(img_bt2,WINDOWWIDTH/10 *7,WINDOWHEIGHT/10 *5,tile_size*2,tile_size*2)
button_x_pause = Button(img_bt5,WINDOWWIDTH/10 *3,WINDOWHEIGHT/10 *5,tile_size*2,tile_size*2)
button_reload_pause = Button(img_bt11,WINDOWWIDTH/10 * 5, WINDOWHEIGHT/10 *5,tile_size*2,tile_size*2)

#detail 
table_detail = Button(img_bt1,WINDOWWIDTH/2,WINDOWHEIGHT/2,550,550)
button_x_detail = Button(img_bt5,WINDOWWIDTH/5 *4,WINDOWHEIGHT/5,tile_size*2,tile_size*2)


#win
victory = Button(img_UI8,WINDOWWIDTH/2,WINDOWHEIGHT/2,530,250)
button_x_win = Button(img_bt5,WINDOWWIDTH/10 *3,WINDOWHEIGHT/2 + WINDOWHEIGHT/5,tile_size*2,tile_size*2)
button_menu_end = Button(img_bt12,WINDOWWIDTH/2,WINDOWHEIGHT/2,600,450)
button_win = Button(img_bt15,int(WINDOWWIDTH/2 + WINDOWWIDTH/8),WINDOWHEIGHT/2 + WINDOWHEIGHT/5,300,80)

#die
lose = Button(img_UI9,WINDOWWIDTH/2,WINDOWHEIGHT/10* 4.5,450,200)
button_x_die = Button(img_bt5,WINDOWWIDTH/10 * 4,WINDOWHEIGHT/10 * 6.5,tile_size*2,tile_size*2)
button_reload_die = Button(img_bt11,WINDOWWIDTH/10 * 6,WINDOWHEIGHT/10 * 6.5,tile_size *2,tile_size*2)

# TEXT
start_text = Text("START",WINDOWWIDTH/10 *1.5 ,WINDOWHEIGHT/10 *8,'PixelGamerPersonalUse-rg61L.otf',40)
exit_text = Text("EXIT",WINDOWWIDTH/10 *8.5,WINDOWHEIGHT/10 *8,'PixelGamerPersonalUse-rg61L.otf',40)
name_text = Text("LABYRINTH",WINDOWWIDTH/2,WINDOWHEIGHT/4 - 20,"PixelGamerPersonalUse-rg61L.otf",128)
next_level = Text("next_level",WINDOWWIDTH/2 + WINDOWWIDTH/8,WINDOWHEIGHT/2 + WINDOWHEIGHT/5,"PixelGamerPersonalUse-rg61L.otf",40)
detail_text = Text(f'press movement keys or ASDW to move',WINDOWWIDTH/10 *5,WINDOWHEIGHT/10 *3,"PixelGamerPersonalUse-rg61L.otf",20)



bg1 = BG(img_bg1,0,0,WINDOWWIDTH,WINDOWHEIGHT,1)
bg2 = BG(img_bg2,0,0,WINDOWWIDTH,WINDOWHEIGHT,1)
player1 = Player(250,250,hero_width,hero_height)

world = World(world_data)
Start, Pause = False,False 
running = True
win, detail = False, False
up, down, left, right = False, False, False, False
mouse_left ,mouse_right = False,False
Pause = False
while running:
    hp_text = Text(f"{player1.hp}",35,26,"VHARIABI.TTF",10)
    if not Start:
        bg1.draw()
        world.draw()
        world.update_animation()
        button_start1.draw()
        button_start2.draw()
        start_text.draw()
        exit_text.draw()
        name_text.draw()

    if Start:
        if not Pause:
            bg2.draw()
            world.draw()
            bg2.draw_menu()
            player1.update_animation()
            world.update_animation()
            player1.draw()
            player1.move(up, down, left, right,world)
            bg2.move(player1,world)
            menu.draw()
            hp_text.draw()
            if win:
                button_menu_end.draw()
                button_x_win.draw()
                victory.draw()
                button_win.draw()
                next_level.draw()
        if Pause:
            button_menu_pause.draw()
            button_play.draw()
            button_x_pause.draw()
            button_reload_pause.draw()
            if detail:
                table_detail.draw()
                button_x_detail.draw()
                detail_text.draw()

        if not player1.alive:
            button_menu_end.draw()
            lose.draw()
            button_x_die.draw()
            button_reload_die.draw()



    if start_text.check():
        Start = True
        level +=1
        with open(f'{dir_data}level_{level}_data.csv', newline = '') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for x, row in enumerate(reader):    
                for y, tile in enumerate(row):
                    world_data[x][y] = int(tile)
            world = World(world_data)
    if Start:
        if menu.check():
            Pause = True
        if Pause:
            if button_x_pause.check():
                running = False
            if button_play.check():
                Pause = False
            if button_reload_pause.check():
                player1.hp = 100
                player1.hero_rect = pygame.Rect(250,250,player1.width,player1.height)
                player1.wind_rect = pygame.Rect(250,250,player1.width,player1.height)
                with open(f'{dir_data}level_{level}_data.csv', newline = '') as csvfile:
                    reader = csv.reader(csvfile, delimiter=',')
                    for x, row in enumerate(reader):
                        for y, tile in enumerate(row):
                            world_data[x][y] = int(tile)
                world = World(world_data)
        if win:
            if next_level.check():
                level +=1
                player1.hp = 100
                player1.hero_rect = pygame.Rect(250,250,player1.width,player1.height)
                player1.wind_rect = pygame.Rect(250,250,player1.width,player1.height)
                win = False
                with open(f'{dir_data}level_{level}_data.csv', newline = '') as csvfile:
                    reader = csv.reader(csvfile, delimiter=',')
                    for x, row in enumerate(reader):
                        for y, tile in enumerate(row):
                            world_data[x][y] = int(tile)
                world = World(world_data)
            if button_x_win.check():
                running = False
        if not player1.alive:
            if button_reload_die.check():
                player1.hp = 100
                player1.hero_rect = pygame.Rect(250,250,player1.width,player1.height)
                player1.wind_rect = pygame.Rect(250,250,player1.width,player1.height)
                win = False
                with open(f'{dir_data}level_{level}_data.csv', newline = '') as csvfile:
                    reader = csv.reader(csvfile, delimiter=',')
                    for x, row in enumerate(reader):
                        for y, tile in enumerate(row):
                            world_data[x][y] = int(tile)
                world = World(world_data)   
            if button_x_die.check():
                running = False    
    if exit_text.check():
        running = False  

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

        if event.type == QUIT:
            pygame.quit()
            running = False
        if event.type == KEYDOWN:
            if player1.jump_check == True:
                if event.key == K_UP or event.key == K_w:
                    up = True
                    player1.vel_y = player1.jump
                    player1.jump_cout +=1
                    if player1.jump_cout >= 2:   # kiểm soát số lượng lần nhảy
                        player1.jump_check = False
            if event.key == K_0:
                level += 1
                with open(f'{dir_data}level_{level}_data.csv', newline = '') as csvfile:
                    reader = csv.reader(csvfile, delimiter=',')
                    for x, row in enumerate(reader):
                        for y, tile in enumerate(row):
                            world_data[x][y] = int(tile)
                world = World(world_data)
            if event.key == K_1:
                level -= 1
                with open(f'{dir_data}level_{level}_data.csv', newline = '') as csvfile:
                    reader = csv.reader(csvfile, delimiter=',')
                    for x, row in enumerate(reader):
                        for y, tile in enumerate(row):
                            world_data[x][y] = int(tile)
                world = World(world_data)
            if event.key == K_j:
                tile_size += 5
            if event.key == K_k:
                tile_size -= 5
            if event.key == K_DOWN or event.key == K_s:
                down = True
            if event.key == K_LEFT or event.key == K_a:
                left = True
            if event.key == K_RIGHT or event.key == K_d:
                right = True
            if event.key == K_SPACE:
                running = False
            if event.key == K_0:
                Start = True
            if event.key == K_1:
                Pause = True
            if event.key == K_2:
                Pause = False

        if event.type == KEYUP:
            if event.key == K_UP or event.key == K_w:
                up = False
            if event.key == K_DOWN or event.key == K_s:
                down = False
            if event.key == K_LEFT or event.key == K_a:
                left = False
            if event.key == K_RIGHT or event.key == K_d:
                right = False
    pygame.display.update()
    fpsclock.tick(FPS)    
  