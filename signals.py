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

class Update(Signal):
    def execute(listener, **kwargs):
        listener.update()

class Move(Signal):
    def execute(listener, **kwargs):
        listener.move()