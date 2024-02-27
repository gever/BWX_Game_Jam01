import entity_player
import entity_skull_monster
import entity_slime_monster
import entity_rock
import entity_pickaxe
import entity_lavablob

def load_entities():
    entity_player.load()
    entity_skull_monster.load()
    entity_slime_monster.load()
    entity_rock.load()
    entity_pickaxe.load()
    entity_lavablob.load()

# maps strings found in the map files to entity classes
ENTITY_MAP = {
    'player_spawn': entity_player.Player,
    'skull_monster': entity_skull_monster.SkullMonster,
    'slime_monster': entity_slime_monster.SlimeMonster,
    'rock': entity_rock.Rock,
    'pickaxe': entity_pickaxe.Pickaxe,
    'lava_blob': entity_lavablob.LavaBlob,
}
