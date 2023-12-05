from asteroids import Asteroid
from enemy import Enemy, EnemyCrazy, EnemyLinear

class EntityFactory():

    @classmethod
    def create_entity(cls, entity_type):
        if entity_type == "asteroid":
            return Asteroid.create()
        elif entity_type == "enemy_linear":
            return EnemyLinear.create()
        elif entity_type == "enemy_crazy":
            return EnemyCrazy.create()
        elif entity_type == "enemy":
            return Enemy.create()