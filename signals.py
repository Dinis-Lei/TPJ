class Signal:
    def execute():
        raise NotImplemented
    
class Nothing(Signal):
    def execute(listener, **kwargs):
        pass    

class Quit(Signal):
    def execute(listener, **kwargs):
        listener.quit() 

class Left(Signal):
    def execute(listener, **kwargs):
        listener.left()

class Right(Signal):
    def execute(listener, **kwargs):
        listener.right()

class Up(Signal):
    def execute(listener, **kwargs):
        listener.up()

class Down(Signal):
    def execute(listener, **kwargs):
        listener.down()

class Shoot(Signal):
    def execute(listener, **kwargs):
        listener.shoot()

class Update(Signal):
    def execute(listener, **kwargs):
        listener.update()