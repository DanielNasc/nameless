import pygame
from settings import *

class Upgrade:
    def __init__(self,player):
        #general setup
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.attribute_nr = len(player.stats)
        self.attribute_names = list(player.stats.keys())
        self.max_values = list(player.max_stats.values())
        self.font = pygame.font.Font(UI_FONT,UI_FONT_SIZE)

        #item creation
        self.height = self.display_surface.get_size()[1] * 0.8
        self.width = self.display_surface.get_size()[0] // 6
        self.creat_items()

        #selection system
        self.selection_index = 0
        self.selection_time = None
        self.can_move = True

    def input(self):
        keys = pygame.key.get_pressed()
        if  self.can_move:
            if keys[pygame.K_RIGHT] and self.selection_index < self.attribute_nr -1:
                self.selection_index += 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()

            elif keys[pygame.K_LEFT] and self.selection_index > 0:
                self.selection_index -= 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()

            if keys[pygame.K_SPACE]:
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
                print(self.selection_index)

    def selecion_cooldown(self):
        if not self.can_move:
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_time >= 300:
                self.can_move = True

    def creat_items(self):
        self.item_list = []

        for item, index in enumerate(range(self.attribute_nr)):
            full_width = self.display_surface.get_size()[0]
            increment = full_width // self.attribute_nr
            left = (item * increment) + (increment - self.width) // 2

            top = self.display_surface.get_size()[1] * 0.1

            item = Item(left,top,self.width,self.height,index,self.font)
            self.item_list.append(item)

    def display(self):
        self.input()
        self.selecion_cooldown()

        for index, item in enumerate(self.item_list):
            name = self.attribute_names[index]
            value = self.player.get_value_by_index(index)
            max_value = self.max_values[index]
            cost = self.player.get_cost_by_index(index)
            item.display(self.display_surface,self.selection_index,name,value,max_value,cost)

class Item:
    def __init__(self,l,t,w,h,index,font):
        self.rect = pygame.Rect(l,t,w,h)
        self.index = index
        self.font = font

    def display_names(self,surface,name,cost,selected):
        color = TEXT_COLOR_SELECTED if selected else UPGRADE_BG_COLOR_SELECTED


        #title
        title_surf = self.font.render(name,False,color)
        title_rect = title_surf.get_rect(midtop = self.rect.midtop + pygame.math.Vector2(0,20))

        #cost
        cost_surf = self.font.render(f'{int(cost)}',False,color)
        cost_rect = cost_surf.get_rect(midbottom = self.rect.midbottom - pygame.math.Vector2(0,20))


        #draw
        surface.blit(title_surf,title_rect)
        surface.blit(cost_surf,cost_rect)

    def display_bar(self,surface,value,max_value,selected):
        
        #drawing setup
        top = self.rect.midtop + pygame.math.Vector2(0,60)
        bottom = self.rect.midbottom - pygame.math.Vector2(0,60)
        color = BAR_COLOR_SELECTED if selected else BAR_COLOR

        #draw elements
        pygame.draw.line(surface,color,top,bottom,5)


    def display(self,surface,selection_num,name, value,max_value,cost):
        if self.index == selection_num:
            pygame.draw.rect(surface, UPGRADE_BG_COLOR_SELECTED ,self.rect)
            pygame.draw.rect(surface, UPGRADE_BORDER_COLOR_ACTIVE,self.rect,4)
        else:
            pygame.draw.rect(surface, UI_BG_COLOR,self.rect)
            pygame.draw.rect(surface, UPGRADE_BORDER_COLOR_ACTIVE,self.rect,4)
        self.display_names(surface,name,cost, self.index == selection_num)
        self.display_bar(surface,value,max_value,self.index == selection_num)