next_collision_type_id = 1
def get_new_collision_type_id():
    global next_collision_type_id
    new_id = next_collision_type_id
    next_collision_type_id += 1
    return new_id

COLLISION_TYPE_ENTITY = get_new_collision_type_id()
COLLISION_TYPE_IMPASSABLE_TILE = get_new_collision_type_id()
COLLISION_TYPE_PARTICLE = get_new_collision_type_id()
