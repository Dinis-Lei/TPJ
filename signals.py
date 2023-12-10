class Signal:
    """ Base class for signals """
    def execute():
        raise NotImplemented
    
class Nothing(Signal):
    def execute(listener, **kwargs):
        pass    

class Quit(Signal):
    def execute(listener, **kwargs):
        listener.quit() 

class Start(Signal):
    def execute(listener, **kwargs):
        listener.start() 

class Accelerate(Signal):
    def execute(listener, **kwargs):
        listener.accelerate()

class Brake(Signal):
    def execute(listener, **kwargs):
        listener.brake()

class Shoot(Signal):
    def execute(listener, **kwargs):
        listener.shoot(frame=kwargs["frame"])

class Pause(Signal):
    def execute(listener, **kwargs):
        listener.pause()

class Display(Signal):
    def execute(listener, **kwargs):
        listener.display()

class Move(Signal):
    def execute(listener, **kwargs):
        listener.move()

class Update(Signal):
    def execute(listener, **kwargs):
        listener.update()

class CheckCollision(Signal):
    def execute(listener, **kwargs):
        listener.check_collision(**kwargs)

class EnemyShoot(Signal):
    def execute(listener, **kwargs):
        listener.enemy_shoot()

class UpdateScore(Signal):
    def execute(listener, **kwargs):
        listener.update_score(score=kwargs['score'])
    
class UpdateLives(Signal):
    def execute(listener, **kwargs):
        listener.update_lives(lives=kwargs["lives"])

class UpdateHighScore(Signal):
    def execute(listener, **kwargs):
        listener.update_highScore()

class UpdateNukes(Signal):
    def execute(listener, **kwargs):
        listener.update_nukes(nukes=kwargs["nukes"])

class Spawn(Signal):
    def execute(listener, **kwargs):
        listener.spawn(frame=kwargs["frame"])

class PlayerPosition(Signal):
    def execute(listener, **kwargs):
        listener.update_player_pos(pos=kwargs["pos"])

class DestroyAll(Signal):
    def execute(listener, **kwargs):
        listener.destroy_all()

class Nuke(Signal):
    def execute(listener, **kwargs):
        listener.nuke(frame=kwargs["frame"])

class CatchPowerUp(Signal):
    def execute(listener, **kwargs):
        listener.power_up(type=kwargs["type"])
    
