class Signal:
    def execute():
        raise NotImplemented
    
class Nothing(Signal):
    def execute(listener, **kwargs):
        pass    

class Quit(Signal):
    def execute(listener, **kwargs):
        listener.quit() 

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
        listener.update_highScore(**kwargs)
    
