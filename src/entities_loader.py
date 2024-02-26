import entity_player
import entity_skull_monster
import entity_slime_monster
import entity_rock
def load_entities():
    entity_player.load()
    entity_skull_monster.load()
    entity_slime_monster.load()
    entity_rock.load
# maps strings found in the map files to entity classes
ENTITY_MAP = {
    'player_spawn': entity_player.Player,
    'skull_monster': entity_skull_monster.SkullMonster,
    'slime_monster': entity_slime_monster.SlimeMonster,
}
