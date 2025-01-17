import pygame

from settings import HEIGHT, WIDTH, ZOOM
from entities.player.player import Player
from entities.player.weapon import Weapon
from support.sprites_support import convert_path

"""
as principais funções dos grupos são

1. armazenar e desenhar sprites
2. chamar o método update

mas você pode mudar adicionar novos metodos ou mudar os existentes extendendo a classe
"""

class YSortCameraGroup(pygame.sprite.Group): # extendendo a classe Group
    def __init__(self, level=None):
        super().__init__()

        # pegar a surface do display
        self.display_surface = pygame.display.get_surface()

        self.offset = pygame.math.Vector2()

        # centro da tela
        self.half_w = self.display_surface.get_width() // 2
        self.half_h = self.display_surface.get_height() // 2

        # criando a surface onde os sprites serão "blitados"
        self.internal_surf_size = (WIDTH, HEIGHT)
        self.internal_surf = pygame.Surface(self.internal_surf_size, pygame.SRCALPHA)
        self.internal_surf_size_vector = pygame.math.Vector2(self.internal_surf_size)
        self.internal_rect = self.internal_surf.get_rect()

        self.filter_surf = pygame.Surface((WIDTH, HEIGHT))
        self.filter_surf.fill((50, 50, 100))
        self.filter_surf.set_alpha(75)

        # criando o floor
        
        if (level):
            self.floor_surface = pygame.image.load(convert_path(f'assets/sprites/background/{level}.png')).convert()
        else:
            self.floor_surface = pygame.surface.Surface((WIDTH, HEIGHT))

        self.floor_rect = self.floor_surface.get_rect(topleft = (0,0))

    def custom_draw(self, player: Player):
        self.offset.x = player.rect.centerx - self.half_w
        self.offset.y = player.rect.centery - self.half_h

        self.internal_surf.fill((0, 0, 0))

        floor_offset = self.floor_rect.topleft - self.offset
        self.internal_surf.blit(self.floor_surface, floor_offset)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.bottom):
            offset_pos = sprite.rect.topleft - self.offset
            self.internal_surf.blit(sprite.image, offset_pos)

        scaled_surf = pygame.transform.scale(self.internal_surf, self.internal_surf_size_vector * ZOOM)
        scaled_rect = scaled_surf.get_rect(center = (self.half_w, self.half_h))

        self.display_surface.blit(scaled_surf, scaled_rect)
        self.display_surface.blit(self.filter_surf, (0, 0))

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == "enemy" ]
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
