class Signal:
    """ Base class for signals """
    def execute():
        raise NotImplemented
    
class Nothing(Signal):
    def execute(listener, **kwargs):
        pass    

""" Signals used to make events more organized.  """

class Quit(Signal):
    """ Used on endgame """
    def execute(listener, **kwargs):
        listener.quit() 

class Start(Signal):
    """ Used on start/restart game """
    def execute(listener, **kwargs):
        listener.start() 

class Accelerate(Signal):
    """ Used to check player acceleration """
    def execute(listener, **kwargs):
        listener.accelerate()

class Brake(Signal):
    """ Used to check player braking """
    def execute(listener, **kwargs):
        listener.brake()

class Shoot(Signal):
    """ Used to check player shooting """
    def execute(listener, **kwargs):
        listener.shoot(frame=kwargs["frame"])

class Display(Signal):
    """ Used to display every entity """
    def execute(listener, **kwargs):
        listener.display()

class Move(Signal):
    """ Used to move entities """
    def execute(listener, **kwargs):
        listener.move()

class Update(Signal):
    """ Used to update entities """
    def execute(listener, **kwargs):
        listener.update()

class CheckCollision(Signal):
    """ Used to check for collisions between two entities """
    def execute(listener, **kwargs):
        listener.check_collision(**kwargs)

class EnemyShoot(Signal):
    """ Used to check enemy shooting """
    def execute(listener, **kwargs):
        listener.enemy_shoot()

class UpdateScore(Signal):
    """ Used to update score on hud """
    def execute(listener, **kwargs):
        listener.update_score(score=kwargs['score'])
    
class UpdateLives(Signal):
    """ Used to update lives on hud """
    def execute(listener, **kwargs):
        listener.update_lives(lives=kwargs["lives"])

class UpdateHighScore(Signal):
    """ Used to update highscore """
    def execute(listener, **kwargs):
        listener.update_highScore(score=kwargs["score"])

class UpdateNukes(Signal):
    """ Used to update nukes on hud """
    def execute(listener, **kwargs):
        listener.update_nukes(nukes=kwargs["nukes"])

class Spawn(Signal):
    """ Used to spawn entities """
    def execute(listener, **kwargs):
        listener.spawn(frame=kwargs["frame"])

class PlayerPosition(Signal):
    """ Used to update player current position"""
    def execute(listener, **kwargs):
        listener.update_player_pos(pos=kwargs["pos"])

class DestroyAll(Signal):
    """ Used to destroy all entites except for player and powerups"""
    def execute(listener, **kwargs):
        listener.destroy_all()

class Nuke(Signal):
    """ Used when player uses nukes """
    def execute(listener, **kwargs):
        listener.nuke(frame=kwargs["frame"])

class CatchPowerUp(Signal):
    """ Used to catch powerups"""
    def execute(listener, **kwargs):
        listener.power_up(type=kwargs["type"])
    
