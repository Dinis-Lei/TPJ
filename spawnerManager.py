from enum import Enum
from asteroids import Asteroid
from enemy import *
from game_vars import *
from powerup import PowerUp
from service_locator import ServiceLocator
from entityFactory import EntityFactory
import random
from signals import *

SPAWER_POOL_BASE = {
    "easy" : {
        "asteroid" : 10,
        "enemy_linear" : 2,
        "powerup" : 1,
    },
    "medium" : {
        "asteroid" : 7,
        "enemy_linear" : 4,
        "enemy_crazy" : 1,
        "powerup" : 2,
    },
    "hard" : {
        "asteroid" : 10,
        "enemy_linear" : 3,
        "enemy_crazy" : 4,
        "powerup" : 2,
    },
}

class DifficultyStates(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class SpawnerManager():

    def __init__(self) -> None:
        self.serv_loc = ServiceLocator.create()
        self.obs = self.serv_loc.get_observer()
        self.obs.subscribe(Spawn, self)

        self.difficulty_state = DifficultyStates.EASY

        self.counter = 0
        self.spawn_interval = 1000
        self.pool = {k: v for k,v in SPAWER_POOL_BASE[self.difficulty_state.value].items()}


    def state_machine(self, frame:int):
        r = random.random()

        if self.difficulty_state == DifficultyStates.EASY:
            if r < 0.3:
                self.difficulty_state = DifficultyStates.EASY
            elif r < 0.9:
                self.difficulty_state = DifficultyStates.MEDIUM
            else:
                self.difficulty_state = DifficultyStates.HARD
        elif self.difficulty_state == DifficultyStates.MEDIUM:
            if r < 0.5:
                self.difficulty_state = DifficultyStates.EASY
            elif r < 0.75:
                self.difficulty_state = DifficultyStates.MEDIUM
            else:
                self.difficulty_state = DifficultyStates.HARD
        elif self.difficulty_state == DifficultyStates.HARD:
            if r < 0.2:
                self.difficulty_state = DifficultyStates.EASY
            elif r < 0.8:
                self.difficulty_state = DifficultyStates.MEDIUM
            else:
                self.difficulty_state = DifficultyStates.HARD


        self.pool = {
            k: min(v+(frame//9000), 10) for k,v in SPAWER_POOL_BASE[self.difficulty_state.value].items()
        }
    

    def spawn(self, frame):
        for entity, amount in self.pool.items():
            c = 0
            for _ in range(amount):
                r = random.randint(self.counter, self.spawn_interval)
                if r >= self.spawn_interval*0.90:
                    # print(f"Spawning {entity}, {amount}")
                    if entity == "asteroid":
                        Asteroid.create()
                    elif entity == "enemy_linear":
                        EnemyLinear.create()
                    elif entity == "enemy_crazy":
                        EnemyCrazy.create()
                    elif entity == "enemy":
                        Enemy.create()
                    elif entity == "powerup":
                        PowerUp.create()
                    c += 1
            self.pool[entity] -= c
        
        self.counter += 1

        if sum(self.pool.values()) == 0:
            self.counter = 0
            self.state_machine(frame)
            print(f"New state: {self.difficulty_state}")