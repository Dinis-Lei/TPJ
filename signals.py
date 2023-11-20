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
        listener.shoot()

class Pause(Signal):
    def execute(listener, **kwargs):
        listener.pause()

class Display(Signal):
    def execute(listener, **kwargs):
        listener.display()

class Move(Signal):
    def execute(listener, **kwargs):
        listener.move()

class CheckCollision(Signal):
    def execute(listener, **kwargs):
        listener.check_collision(**kwargs)