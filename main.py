from core.game import Game
from map.generator import MapGenerator

def main():
    gm = Game()

if __name__ == "__main__":
    generator = MapGenerator("config/game_config.json")
    game_map = generator.generate()

    for y in range(game_map.height):
        row = []
        for x in range(game_map.width):
            if game_map.objects[x][y] is not None:
                row.append(game_map.objects[x][y])
            else:
                row.append(game_map.tiles[x][y])
        print("".join(row))