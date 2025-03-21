from Const_Values import *
from Door import Door

class World:
    def __init__(self, data, door_group):
        self.tile_list = []
        self.door_group = door_group
        block_img = pygame.image.load('img/platform1.png')

        for row_count, row in enumerate(data):
            for col_count, tile in enumerate(row):
                if tile == 1:
                    img = pygame.transform.scale(block_img, (tile_size, tile_size))
                    img_rect = img.get_rect(topleft=(col_count * tile_size, row_count * tile_size))
                    self.tile_list.append((img, img_rect))
                if tile == 2:
                    door = Door(col_count * tile_size, row_count * tile_size - (tile_size // 2))
                    self.door_group.add(door)

    def draw(self, screen):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
        self.door_group.draw(screen)