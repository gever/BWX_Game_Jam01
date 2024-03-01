import entity_player
import entity_bat_monster
import entity_slime_monster
import entity_rock
import entity_pickaxe
import entity_lavablob
import entity_waterblob

def load_entities():
    entity_player.load()
    entity_bat_monster.load()
    entity_slime_monster.load()
    entity_rock.load()
    entity_pickaxe.load()
    entity_lavablob.load()
    entity_waterblob.load()

# maps strings found in the map files to entity classes
ENTITY_MAP = {
    'player_spawn': entity_player.Player,
    'skull_monster': entity_bat_monster.BatMonster,
    'slime_monster': entity_slime_monster.SlimeMonster,
    'rock': entity_rock.Rock,
    'pickaxe': entity_pickaxe.Pickaxe,
    'lava_blob': entity_lavablob.LavaBlob,
    'water_blob': entity_waterblob.WaterBlob,
}
